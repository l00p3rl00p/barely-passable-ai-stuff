//! UKC/1 admission. Parser reports are retained literally alongside the source's hash.
//! Native parser output is never inferred from a different parser. OmniGraph is a
//! keyed projection of the same canonical records, not a second interpretation.
use anyhow::{anyhow, Context, Result};
use pulldown_cmark::{Event, Options, Parser, Tag, TagEnd};
use rayon::prelude::*;
use regex::Regex;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::{collections::{BTreeMap, HashSet}, fs, path::{Path,PathBuf}, time::Instant};
use walkdir::{DirEntry, WalkDir};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Record {
    pub schema: String,
    pub id: String,
    pub source: Value,
    pub kind: String,
    pub location: Value,
    pub relations: Vec<Value>,
    pub proximity: Value,
    pub values: Value,
    pub native: Value,
    pub evidence: Value,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Edge {
    pub from: String,
    pub to: String,
    pub relation: String,
    pub origin: String,
    pub evidence_key: String,
}
#[derive(Debug, Serialize, Deserialize)]
pub struct Scan {
    pub records: Vec<Record>,
    pub edges: Vec<Edge>,
    pub files_seen: usize,
    pub errors: Vec<String>,
    pub skipped: Vec<String>,
    pub scan_seconds: f64,
}

pub fn sha(raw: &[u8]) -> String { format!("{:x}", Sha256::digest(raw)) }

/// UKC-ID-1: SHA256 of compact UTF-8 JSON array with six ordered strings.
pub fn canonical_id(authority: &str, key: &str, version: &str, kind: &str, unit: &str) -> String {
    let payload = serde_json::to_vec(&["ukc/1", authority, key, version, kind, unit]).expect("UTF-8 array");
    format!("ukc:v1:{}", sha(&payload))
}
fn checksum_span(raw: &[u8], start: usize, end: usize) -> Result<String> {
    if start > end || end > raw.len() { return Err(anyhow!("invalid span")); }
    Ok(sha(&raw[start..end]))
}
fn is_skipped(e: &DirEntry) -> bool {
    // Only infrastructure-generated directories are excluded; all other files,
    // including unknown binary types, must appear in the coverage report.
    e.file_type().is_dir() && matches!(e.file_name().to_str().unwrap_or(""),
        ".git" | "node_modules" | "target" | ".venv" | "venv" | "__pycache__" | ".cache")
}
fn line_at(raw: &[u8], byte: usize) -> usize {
    1 + raw[..byte.min(raw.len())].iter().filter(|b| **b == b'\n').count()
}
fn headline(text: &str) -> String { text.trim().chars().take(200).collect() }

fn parser_report(ext: &str, raw: &[u8]) -> (String, Value, Vec<(usize, usize, String)>) {
    let Ok(text) = std::str::from_utf8(raw) else {
        return ("none:non-utf8".into(), Value::Null, vec![]);
    };
    match ext {
        "md" | "mdx" => {
            // OffsetIterator positions are byte ranges within the original UTF-8 source.
            // Event debug strings preserve the exact events yielded by pulldown-cmark;
            // no DOM, AST or semantic relationships are invented from them.
            let mut tokens = Vec::new();
            let mut headings: Vec<(usize, usize, String)> = Vec::new();
            let mut active: Option<(usize, u8, String)> = None;
            for (evt, span) in Parser::new_ext(text, Options::all()).into_offset_iter() {
                let description = format!("{evt:?}");
                match &evt {
                    Event::Start(Tag::Heading { level, .. }) => {
                        let n = match level { pulldown_cmark::HeadingLevel::H1 => 1,
                            pulldown_cmark::HeadingLevel::H2 => 2,
                            pulldown_cmark::HeadingLevel::H3 => 3,
                            pulldown_cmark::HeadingLevel::H4 => 4,
                            pulldown_cmark::HeadingLevel::H5 => 5,
                            pulldown_cmark::HeadingLevel::H6 => 6 };
                        active = Some((span.start, n, String::new()));
                    }
                    Event::Text(t) | Event::Code(t) => {
                        if let Some((_, _, heading)) = &mut active { heading.push_str(t); }
                    }
                    Event::End(TagEnd::Heading(_)) => {
                        if let Some((start, _, title)) = active.take() {
                            headings.push((start, span.end, headline(&title)));
                        }
                    }
                    _ => {}
                }
                tokens.push(json!({"start_byte":span.start,"end_byte":span.end,"event":description}));
            }
            ("pulldown-cmark/0.12".to_string(), json!(tokens), headings)
        }
        "json" => match serde_json::from_str::<Value>(text) {
            Ok(v) => ("serde_json".into(), v, vec![]),
            Err(err) => (format!("serde_json:parse-error:{err}"), Value::Null, vec![]),
        },
        "csv" => {
            let mut rdr = csv::ReaderBuilder::new().flexible(true).from_reader(raw);
            let names = match rdr.headers() { Ok(h) => h.iter().map(str::to_string).collect::<Vec<_>>(),
                Err(e) => return (format!("csv:parse-error:{e}"), Value::Null, vec![]) };
            let mut rows = Vec::new();
            for row in rdr.records() {
                match row { Ok(r) => rows.push(r.iter().map(str::to_string).collect::<Vec<_>>()),
                    Err(e) => return (format!("csv:parse-error:{e}"), Value::Null, vec![]) }
            }
            ("csv::Reader".into(), json!({"fieldnames":names,"rows":rows}), vec![])
        }
        _ => ("none:original-source-preserved".into(), Value::Null, vec![]),
    }
}

/// A cheap, deterministic lexical projection; it is NOT a neural embedding.
/// Same STOP and hash/sign behavior as the checked-in original Rust scanner.
pub fn lexical_hash_512(text: &str) -> Vec<f32> {
    const STOP: &[&str] = &["the","and","that","this","with","from","for","are","was","were","into","not",
        "but","can","may","its","their","they","our","has","have","had","only","than",
        "when","what","which","while","where","how","use","uses","using","used","one",
        "two","three","more","also","does","each","such","these","those","been","being",
        "should","would","could","will","must","all","any","per","through","without"];
    let stop: HashSet<&str> = STOP.iter().copied().collect();
    let re = Regex::new(r"\w+").unwrap();
    let mut v = vec![0f32; 512];
    let lowered=text.to_lowercase();
    for m in re.find_iter(&lowered) {
        let w = m.as_str();
        if stop.contains(w) { continue; }
        let d = Sha256::digest(w.as_bytes());
        let idx = (u32::from_be_bytes([d[0],d[1],d[2],d[3]]) % 512) as usize;
        v[idx] += if d[4] % 2 == 0 { 1. } else { -1. };
    }
    let n = v.iter().map(|x| x*x).sum::<f32>().sqrt();
    if n > 0. { for x in &mut v { *x /= n; } }
    v
}
fn words(text: &str) -> String {
    let re = Regex::new(r"[a-z0-9][a-z0-9_-]{2,}").unwrap();
    let mut counts = BTreeMap::<String, usize>::new();
    let lowered=text.to_lowercase();
    for m in re.find_iter(&lowered) { *counts.entry(m.as_str().to_string()).or_default() += 1; }
    let mut terms: Vec<_> = counts.into_iter().collect();
    terms.sort_by(|a,b| b.1.cmp(&a.1).then(a.0.cmp(&b.0)));
    terms.into_iter().take(24).map(|(w,_)| w).collect::<Vec<_>>().join(" ")
}
fn record(raw: &[u8], authority: &str, rel: &str, span: (usize, usize),
          kind: &str, unit: &str, title: Option<String>, parser_name: &str, native: Value) -> Result<Record> {
    let source_sha = sha(raw);
    let span_sha = checksum_span(raw, span.0, span.1)?;
    let id = canonical_id(authority, rel, &source_sha, kind, unit);
    let text = std::str::from_utf8(&raw[span.0..span.1]).unwrap_or("");
    let filename = Path::new(rel).file_name().unwrap_or_default().to_string_lossy().into_owned();
    // A binary or empty source has no parsed content; its actual filename remains a
    // legitimate lexical discovery surface without claiming any content semantics.
    let proximity_text = if text.trim().is_empty() { filename.as_str() } else { text };
    let start_line = line_at(raw,span.0);
    let end_line = line_at(raw,span.1);
    let values = json!({"name":title.as_deref().unwrap_or(&filename),"filename":filename,
        "title":title,"terms":words(proximity_text)});
    let source = json!({"authority":authority,"key":rel,"version":source_sha,
        "original_bytes":raw.len(),"original_sha256":source_sha});
    let location = json!({"unit":"utf8_byte","start_byte":span.0,"end_byte":span.1,
        "start_line":start_line,"end_line":end_line,"basis":"reader","precision":"parsed"});
    let proximity = json!({"space":"lexical-hash-512/rust-scanner-v1",
        "status":"known","vector":lexical_hash_512(proximity_text)});
    let evidence = json!({"span_sha256":span_sha,"parser":parser_name,
        "source_sha256":source_sha,"native_payload_digest":sha(native.to_string().as_bytes())});
    Ok(Record {schema:"ukc/1".into(),id,source,kind:kind.into(),location,
        relations:vec![],proximity,values,native,evidence})
}
fn scan_file(root: &Path, path: &Path, authority: &str) -> Result<(Vec<Record>,Vec<Edge>)> {
    let rel = path.strip_prefix(root)?.to_string_lossy().replace('\\',"/");
    let raw = fs::read(path).with_context(|| format!("read {}",path.display()))?;
    let ext = path.extension().and_then(|x|x.to_str()).unwrap_or("").to_ascii_lowercase();
    let (parser_name,native,headings) = parser_report(&ext,&raw);
    let mut records=vec![record(&raw,authority,&rel,(0,raw.len()),"file","file",None,&parser_name,native)?];
    let mut edges=vec![];
    let mut previous: Option<String> = None;
    let mut ordinal = BTreeMap::<String,usize>::new();
    // Only meaningful section headings get their own knowledge identities.
    // Full native token/event output stays on the file record: no 400 nodes/file explosion.
    for (i,(start,_end,title)) in headings.iter().enumerate() {
        let end = headings.get(i+1).map(|h|h.0).unwrap_or(raw.len());
        let n = ordinal.entry(title.clone()).or_insert(0); *n+=1;
        let unit=format!("heading:{title}:{}",*n);
        let heading=record(&raw,authority,&rel,(*start,end),"heading_section",&unit,
                           Some(title.clone()),&parser_name,json!({"parser_output":"stored_in_file_record","unit_key":unit}))?;
        edges.push(Edge{from:records[0].id.clone(),to:heading.id.clone(),relation:"contains".into(),
            origin:"native:markdown-heading".into(),evidence_key:sha(unit.as_bytes())});
        if let Some(old)=previous {
            edges.push(Edge{from:old,to:heading.id.clone(),relation:"next_section".into(),
                origin:"native:markdown-order".into(),evidence_key:sha(format!("{unit}:next").as_bytes())});
        }
        previous=Some(heading.id.clone());
        records.push(heading);
    }
    Ok((records,edges))
}

pub fn scan_directory(root: &Path, authority: &str) -> Result<Scan> {
    let t=Instant::now();
    let canonical=root.canonicalize().with_context(|| format!("root {}",root.display()))?;
    if !canonical.is_dir() { return Err(anyhow!("root is not a directory")); }
    if authority.trim().is_empty(){return Err(anyhow!("authority must not be empty"));}
    let mut files=vec![]; let mut skipped=vec![]; let mut errors=vec![];
    for entry in WalkDir::new(&canonical).follow_links(false).into_iter().filter_entry(|e|!is_skipped(e)) {
        match entry {
            Ok(e) if e.file_type().is_file() => files.push(e.into_path()),
            Ok(e) if e.file_type().is_symlink() => skipped.push(format!("symlink (not traversed): {}",e.path().display())),
            Ok(_) => {},
            Err(e) => errors.push(format!("walk error: {e}")),
        }
    }
    files.sort();
    let results:Vec<_> = files.par_iter().map(|p|scan_file(&canonical,p,authority)).collect();
    let mut records=vec![];let mut edges=vec![];
    for (p,r) in files.iter().zip(results){match r{Ok((mut rs,mut es))=>{records.append(&mut rs);edges.append(&mut es)},
        Err(e)=>errors.push(format!("{}: {e:#}",p.display()))}}
    // Coverage must fail closed; a missing file is not a successful full ingestion.
    Ok(Scan{records,edges,files_seen:files.len(),errors,skipped,scan_seconds:t.elapsed().as_secs_f64()})
}

/// This is the actual OmniGraph v0.15 native NDJSON shape; not an invented API.
/// The projection is deliberately thin. Original UKC records are kept in a
/// same-ID NDJSON sidecar; native source and mapping are not reinterpreted.
pub fn omnigraph_records(scan: &Scan, root: &Path) -> Vec<String> {
    let mut out=Vec::new();
    for r in &scan.records {
        let source=r.source.as_object().unwrap();
        let loc=r.location.as_object().unwrap();
        let values=r.values.as_object().unwrap();
        let vec=&r.proximity["vector"];
        let rel_path=source["key"].as_str().unwrap_or("");
        let original=root.join(rel_path);
        let address=original.to_string_lossy().to_string();
        let routes=json!([{"environment":"local","via":"local_file","locator":address}]).to_string();
        let row=json!({"type":"KnowledgeItem","data":{
            "id":r.id,"kind":r.kind,"heading":values["name"],"terms":values["terms"],
            "owner_namespace":source["authority"],
            "source_id":format!("{}:{}",source["authority"].as_str().unwrap_or(""),source["key"].as_str().unwrap_or("")),
            "source_path":source["key"],"source_address":address,"possible_routes":routes,
            "source_version_sha256":source["version"],"span_sha256":r.evidence["span_sha256"],
            "source_precision":"verified","position_unit":"utf8_byte",
            "start_byte":loc["start_byte"],"end_byte":loc["end_byte"],
            "start_line":loc["start_line"],"end_line":loc["end_line"],
            "location_method":"source_span","location_basis":"reader","location_precision":"parsed",
            "vector_lexical_hash_512_status":"known","vector_lexical_hash_512":vec,
            "status":"current","enrichment_touches":1,"enrichment_touch_limit":3,"enrichment_frozen":false,
            "realm":"repository"
        }});
        out.push(row.to_string());
    }
    for e in &scan.edges {
        out.push(json!({"edge":"Relationship","from":e.from,"to":e.to,
            "data":{"relation":e.relation,"origin":e.origin,"qualification":"source_structure",
                    "status":"observed","evidence_key":e.evidence_key}}).to_string());
    }
    out
}

pub fn verify_scan(scan:&Scan)->Result<()> {
    if !scan.errors.is_empty(){return Err(anyhow!("{} scan errors: {}",scan.errors.len(),scan.errors.join(" | ")));}
    let ids:HashSet<_>=scan.records.iter().map(|r|&r.id).collect();
    if ids.len()!=scan.records.len(){return Err(anyhow!("duplicate knowledge ids"));}
    for r in &scan.records{
        if r.schema!="ukc/1"||r.id.len()!=71||r.source["version"].as_str().unwrap_or("").len()!=64{
            return Err(anyhow!("invalid record identity/version"));
        }
        let l=&r.location;
        if l["start_byte"].as_u64().unwrap_or(u64::MAX)>l["end_byte"].as_u64().unwrap_or(0){
            return Err(anyhow!("invalid span for {}",r.id));
        }
    }
    for e in &scan.edges {if !ids.contains(&e.from)||!ids.contains(&e.to){return Err(anyhow!("edge endpoint missing"));}}
    Ok(())
}
