use anyhow::{anyhow, Context, Result};
use clap::{Parser,Subcommand};
use serde_json::{json,Value};
use std::{fs,io::Write,path::{Path,PathBuf},process::{Command,Stdio},thread,time::{Duration,Instant}};
use ukc_ingest::{omnigraph_records,scan_directory,verify_scan,Scan};

#[derive(Parser)]
#[command(name="ukc-ingest",about="Source-faithful UKC/1 native ingester; no LinkML or LLM")]
struct Cli {
    #[command(subcommand)] cmd:Cmd,
    #[arg(long)] root:PathBuf,
    #[arg(long,default_value="repo:quatrus-scratchpad")] authority:String,
    #[arg(long)] output:Option<PathBuf>,
    #[arg(long,default_value_t=30)] deadline_seconds:u64,
}
#[derive(Subcommand)]
enum Cmd {
    Scan,
    Ingest {
        #[arg(long,default_value="kp-agent")] target:String,
        #[arg(long,default_value="knowledge")] graph:String,
        #[arg(long,default_value="kp-working")] branch:String,
        #[arg(long,default_value="omnigraph")] omnigraph:String,
    },
}
fn atomic_records(path:&Path,scan:&Scan)->Result<()> {
    let parent=path.parent().filter(|p|!p.as_os_str().is_empty()).unwrap_or_else(||Path::new("."));
    fs::create_dir_all(parent)?;
    let tmp=path.with_extension(format!("ukc-tmp-{}",std::process::id()));
    let res=(||->Result<()>{
        let mut f=fs::File::create(&tmp)?;
        for r in &scan.records { serde_json::to_writer(&mut f,r)?; f.write_all(b"\n")?; }
        f.sync_all()?;
        fs::rename(&tmp,path)?;
        Ok(())
    })();
    if res.is_err(){let _=fs::remove_file(&tmp);}
    res
}
/// Bound the process itself, not just the network request. Spool responses to files
/// so a verbose native load receipt cannot fill a pipe and deadlock.
fn run_bounded(mut cmd:Command,deadline:Instant)->Result<Value> {
    if Instant::now()>=deadline{return Err(anyhow!("ingestion deadline exceeded before command"));}
    let base=std::env::temp_dir().join(format!("ukc-cmd-{}",std::process::id()));
    fs::create_dir_all(&base)?;
    let stdout=base.join("stdout.txt");
    let stderr=base.join("stderr.txt");
    let result=(||->Result<Value>{
        cmd.stdout(Stdio::from(fs::File::create(&stdout)?))
            .stderr(Stdio::from(fs::File::create(&stderr)?));
        let mut child=cmd.spawn().context("launching native OmniGraph CLI")?;
        loop {
            if let Some(status)=child.try_wait()? {
                let out=fs::read_to_string(&stdout).unwrap_or_default();
                let err=fs::read_to_string(&stderr).unwrap_or_default();
                if !status.success() {
                    return Err(anyhow!("OmniGraph CLI exit {}: {}",status,err.chars().take(1200).collect::<String>()));
                }
                return serde_json::from_str(out.trim())
                    .with_context(||format!("unrecognized native CLI response: {}",out.chars().take(500).collect::<String>()));
            }
            if Instant::now()>=deadline {
                let _=child.kill();let _=child.wait();
                return Err(anyhow!("30-second deadline exceeded; some working-branch commits may have succeeded"));
            }
            thread::sleep(Duration::from_millis(40));
        }
    })();
    let _=fs::remove_dir_all(&base);
    result
}
fn load(scan:&Scan,root:&Path,target:&str,graph:&str,branch:&str,exe:&str,deadline:Instant)->Result<(usize,Value)> {
    let rows=omnigraph_records(scan,root);
    let mut loaded=0usize;
    let mut last=Value::Null;
    let dir=std::env::temp_dir().join(format!("ukc-load-{}",std::process::id()));
    fs::create_dir_all(&dir)?;
    let result=(||->Result<(usize,Value)> {
        let mut offset=0usize;
        let mut batch=0usize;
        while offset<rows.len() {
            let mut end=offset;
            let mut size=0usize;
            while end<rows.len() && end-offset<4000 {
                let bytes=rows[end].len()+1;
                if bytes>24*1024*1024 {return Err(anyhow!("one projected record exceeds native 24MiB limit"));}
                if end>offset && size+bytes>24*1024*1024 {break;}
                size+=bytes;
                end+=1;
            }
            let path=dir.join(format!("batch-{batch:05}.ndjson"));
            let mut f=fs::File::create(&path)?;
            for row in &rows[offset..end] {f.write_all(row.as_bytes())?;f.write_all(b"\n")?;}
            f.sync_all()?;
            drop(f);
            let mut cmd=Command::new(exe);
            cmd.args(["load","--data"]).arg(&path)
                .args(["--mode","merge","--target",target,"--graph",graph,"--branch",branch,"--json"]);
            last=run_bounded(cmd,deadline)?;
            if last.get("error").is_some() {return Err(anyhow!("native load error: {last}"));}
            loaded+=end-offset;
            fs::remove_file(&path)?;
            offset=end;
            batch+=1;
        }
        Ok((loaded,last))
    })();
    let _=fs::remove_dir_all(&dir);
    result
}
fn verify_query(id:&str,target:&str,graph:&str,branch:&str,exe:&str,deadline:Instant)->Result<Value> {
    let mut cmd=Command::new(exe);
    cmd.args(["query","item","--params"]).arg(json!({"id":id}).to_string())
        .args(["--target",target,"--graph",graph,"--branch",branch,"--json"]);
    let response=run_bounded(cmd,deadline)?;
    if !response.to_string().contains(id) {
        return Err(anyhow!("post-commit item lookup did not return the inserted canonical ID"));
    }
    Ok(response)
}
fn main()->Result<()> {
    let cli=Cli::parse();
    let start=Instant::now();
    if cli.deadline_seconds==0{return Err(anyhow!("deadline must be positive"));}
    let deadline=start+Duration::from_secs(cli.deadline_seconds);
    let root=cli.root.canonicalize()?;
    let output=cli.output.unwrap_or_else(||root.parent().unwrap_or(Path::new(".")).join("ukc-output/records.ndjson"));
    // The full logical representation is not a second graph or vector interpretation.
    let scan=scan_directory(&root,&cli.authority)?;
    verify_scan(&scan)?;
    if scan.records.is_empty(){return Err(anyhow!("zero admitted records"));}
    if Instant::now()>=deadline{return Err(anyhow!("scan exceeded the ingestion deadline"));}
    atomic_records(&output,&scan)?;
    match cli.cmd {
        Cmd::Scan=>{
            let elapsed=start.elapsed().as_secs_f64();
            println!("{}",json!({"status":if elapsed<cli.deadline_seconds as f64{"PASS"}else{"FAIL"},
                "files_seen":scan.files_seen,"records":scan.records.len(),"edges":scan.edges.len(),
                "scan_seconds":scan.scan_seconds,"elapsed_seconds":elapsed,
                "native_records":output,"excluded":scan.skipped,"errors":scan.errors}));
            if elapsed>=cli.deadline_seconds as f64 {return Err(anyhow!("scan exceeded deadline"));}
        }
        Cmd::Ingest{target,graph,branch,omnigraph}=>{
            if branch=="main" {return Err(anyhow!("refusing direct writes to protected main"));}
            let (loaded,receipt)=load(&scan,&root,&target,&graph,&branch,&omnigraph,deadline)?;
            if loaded!=scan.records.len()+scan.edges.len(){return Err(anyhow!("native load incomplete"));}
            let check=verify_query(&scan.records[0].id,&target,&graph,&branch,&omnigraph,deadline)?;
            let elapsed=start.elapsed().as_secs_f64();
            let pass=elapsed<cli.deadline_seconds as f64;
            println!("{}",json!({"status":if pass{"PASS"}else{"FAIL"},
                "elapsed_seconds":elapsed,"files_seen":scan.files_seen,
                "records":scan.records.len(),"edges":scan.edges.len(),"loaded":loaded,
                "verified_id":scan.records[0].id,"branch":branch,
                "native_records":output,"receipt":receipt,"query":check}));
            if !pass {return Err(anyhow!("ingestion exceeded {} seconds",cli.deadline_seconds));}
        }
    }
    Ok(())
}
