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
    #[arg(long="target-seconds",alias="deadline-seconds",default_value_t=30,global=true)] target_seconds:u64,
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
/// Performance is an observation, never an ingestion cancellation condition.
fn warn_if_slow(start:Instant,target:Duration,warned:&mut bool,phase:&str) {
    if !*warned && start.elapsed()>=target {
        *warned=true;
        eprintln!("WARNING: UKC ingestion crossed the {}s performance target during {}; continuing to completion",target.as_secs(),phase);
    }
}

/// Capture native CLI output without pipe deadlock. A slow server stays alive;
/// errors and unsuccessful exit statuses still terminate the run.
fn run_native(mut cmd:Command,start:Instant,target:Duration,warned:&mut bool,phase:&str)->Result<Value> {
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
            warn_if_slow(start,target,warned,phase);
            thread::sleep(Duration::from_millis(40));
        }
    })();
    let _=fs::remove_dir_all(&base);
    result
}
fn load(scan:&Scan,root:&Path,target_name:&str,graph:&str,branch:&str,exe:&str,start:Instant,target:Duration,warned:&mut bool)->Result<(usize,usize,Value)> {
    let rows=omnigraph_records(scan,root);
    let mut loaded=0usize;
    let mut last=Value::Null;
    let dir=std::env::temp_dir().join(format!("ukc-load-{}",std::process::id()));
    fs::create_dir_all(&dir)?;
    let result=(||->Result<(usize,usize,Value)> {
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
            let file=dir.join(format!("batch-{batch:05}.ndjson"));
            let mut f=fs::File::create(&file)?;
            for row in &rows[offset..end] {f.write_all(row.as_bytes())?;f.write_all(b"\n")?;}
            f.sync_all()?;
            drop(f);
            let mut cmd=Command::new(exe);
            cmd.args(["load","--data"]).arg(&file)
                .args(["--mode","merge","--target",target_name,"--graph",graph,"--branch",branch,"--json"]);
            last=run_native(cmd,start,target,warned,"native bulk load")?;
            if last.get("error").is_some() {return Err(anyhow!("native load error: {last}"));}
            loaded+=end-offset;
            fs::remove_file(&file)?;
            offset=end;
            batch+=1;
            warn_if_slow(start,target,warned,"native bulk load");
        }
        Ok((loaded,batch,last))
    })();
    let _=fs::remove_dir_all(&dir);
    result
}
fn verify_query(id:&str,target_name:&str,graph:&str,branch:&str,exe:&str,start:Instant,target:Duration,warned:&mut bool)->Result<Value> {
    let mut cmd=Command::new(exe);
    cmd.args(["query","item","--params"]).arg(json!({"id":id}).to_string())
        .args(["--target",target_name,"--graph",graph,"--branch",branch,"--json"]);
    let response=run_native(cmd,start,target,warned,"post-commit verification")?;
    if !response.to_string().contains(id) {
        return Err(anyhow!("post-commit item lookup did not return the inserted canonical ID"));
    }
    Ok(response)
}
fn main()->Result<()> {
    let cli=Cli::parse();
    let start=Instant::now();
    if cli.target_seconds==0{return Err(anyhow!("performance target must be positive"));}
    let target=Duration::from_secs(cli.target_seconds);
    let mut warned=false;
    let root=cli.root.canonicalize()?;
    let output=cli.output.unwrap_or_else(||root.parent().unwrap_or(Path::new(".")).join("ukc-output/records.ndjson"));
    let scan=scan_directory(&root,&cli.authority)?;
    verify_scan(&scan)?;
    if scan.records.is_empty(){return Err(anyhow!("zero admitted records"));}
    let after_scan=start.elapsed();
    warn_if_slow(start,target,&mut warned,"source scan and validation");
    atomic_records(&output,&scan)?;
    let after_write=start.elapsed();
    warn_if_slow(start,target,&mut warned,"source-backed record persistence");
    match cli.cmd {
        Cmd::Scan=>{
            let elapsed=start.elapsed().as_secs_f64();
            println!("{}",json!({"status":"COMPLETE",
                "performance_target_met":elapsed<target.as_secs_f64(),
                "performance_target_seconds":cli.target_seconds,
                "files_seen":scan.files_seen,"records":scan.records.len(),"edges":scan.edges.len(),
                "scan_seconds":scan.scan_seconds,"elapsed_seconds":elapsed,
                "phases_seconds":{"scan_and_validation":after_scan.as_secs_f64(),
                    "record_persistence":(after_write-after_scan).as_secs_f64()},
                "native_records":output,"excluded":scan.skipped,"errors":scan.errors}));
        }
        Cmd::Ingest{target:server_target,graph,branch,omnigraph}=>{
            if branch=="main" {return Err(anyhow!("refusing direct writes to protected main"));}
            let (loaded,batches,receipt)=load(&scan,&root,&server_target,&graph,&branch,&omnigraph,start,target,&mut warned)?;
            if loaded!=scan.records.len()+scan.edges.len(){return Err(anyhow!("native load incomplete"));}
            let after_load=start.elapsed();
            let check=verify_query(&scan.records[0].id,&server_target,&graph,&branch,&omnigraph,start,target,&mut warned)?;
            let elapsed=start.elapsed().as_secs_f64();
            let under_target=elapsed<target.as_secs_f64();
            warn_if_slow(start,target,&mut warned,"final verification");
            println!("{}",json!({"status":"COMPLETE",
                "performance_target_met":under_target,
                "performance_target_seconds":cli.target_seconds,
                "performance_warning":if under_target {Value::Null}
                    else {json!("end-to-end target exceeded; ingestion nevertheless completed")},
                "elapsed_seconds":elapsed,"files_seen":scan.files_seen,
                "records":scan.records.len(),"edges":scan.edges.len(),"loaded":loaded,
                "load_batches":batches,
                "phases_seconds":{"scan_and_validation":after_scan.as_secs_f64(),
                    "record_persistence":(after_write-after_scan).as_secs_f64(),
                    "bulk_load":(after_load-after_write).as_secs_f64(),
                    "verification":(start.elapsed()-after_load).as_secs_f64()},
                "verified_id":scan.records[0].id,"branch":branch,
                "native_records":output,"receipt":receipt,"query":check}));
        }
    }
    Ok(())
}

#[cfg(test)]
mod cli_tests {
    use super::*;
    #[test]
    fn performance_target_flag_after_ingest_is_accepted() {
        let args=Cli::try_parse_from(["ukc-ingest","--root",".","ingest",
            "--target","kp-agent","--target-seconds","30"]);
        assert!(args.is_ok(),"documented CLI invocation must parse");
    }
}
