use std::{fs,collections::HashSet};
use ukc_ingest::{scan_directory,verify_scan,canonical_id,omnigraph_records,lexical_hash_512,export_okf,import_okf};

#[test]
fn cold_mixed_source_roundtrip(){
    let tmp=tempfile::tempdir().unwrap();
    fs::create_dir(tmp.path().join("docs")).unwrap();
    fs::write(tmp.path().join("docs/m.md"),"# Alpha\nA paragraph.\n## Beta\n[See](target.md)\n").unwrap();
    fs::write(tmp.path().join("data.csv"),"id,size\nS01,8\n").unwrap();
    fs::write(tmp.path().join("opaque.wasm"),[0,97,115,109,1,0,0,0]).unwrap();
    fs::write(tmp.path().join("meta.json"),r#"{"answer":42}"#).unwrap();
    let run=scan_directory(tmp.path(),"repo:fixture").unwrap();
    verify_scan(&run).unwrap();
    assert_eq!(run.files_seen,4);
    assert_eq!(run.records.iter().filter(|r|r.kind=="file").count(),4);
    assert_eq!(run.records.iter().filter(|r|r.kind=="heading_section").count(),2);
    assert_eq!(run.edges.iter().filter(|e|e.relation=="contains").count(),2);
    assert_eq!(run.edges.iter().filter(|e|e.relation=="next_section").count(),1);
    assert!(run.records.iter().any(|r|r.source["key"]=="opaque.wasm" && r.native.is_null()));
    let binary=run.records.iter().find(|r|r.source["key"]=="opaque.wasm").unwrap();
    assert!(binary.values["terms"].as_str().unwrap().contains("opaque"));
    assert_eq!(binary.proximity["vector"].as_array().unwrap().len(),512);
    let md=run.records.iter().find(|r|r.source["key"]=="docs/m.md" && r.kind=="file").unwrap();
    assert!(md.native.as_array().unwrap().iter().any(|v|v["event"].as_str().unwrap().contains("Link")));
    let csv=run.records.iter().find(|r|r.source["key"]=="data.csv").unwrap();
    assert_eq!(csv.native["rows"][0][1],"8");
    assert_eq!(run.records.iter().map(|r|&r.id).collect::<HashSet<_>>().len(),run.records.len());
    let payload=serde_json::to_string(&run.records).unwrap();
    let recovered:Vec<ukc_ingest::Record>=serde_json::from_str(&payload).unwrap();
    assert_eq!(recovered.len(),run.records.len());
    assert_eq!(recovered[0].native,run.records[0].native);
    let okf=export_okf(&run.records[0]).unwrap();
    assert_eq!(okf["type"],"SourceUnit");
    let imported=import_okf(&okf).unwrap();
    assert_eq!(serde_json::to_value(&imported).unwrap(),serde_json::to_value(&run.records[0]).unwrap());
    assert!(import_okf(&serde_json::json!({"type":"SourceUnit","title":"fake"})).is_err());
    let rows=omnigraph_records(&run,tmp.path());
    assert_eq!(rows.len(),run.records.len()+run.edges.len());
    assert!(rows.iter().all(|s|serde_json::from_str::<serde_json::Value>(s).is_ok()));
}
#[test]
fn deterministic_id_and_lexical_space(){
    assert_eq!(canonical_id("repo:a","a.md","deadbeef","file","file"),
               canonical_id("repo:a","a.md","deadbeef","file","file"));
    assert_ne!(canonical_id("repo:a","a.md","deadbeef","file","file"),
               canonical_id("repo:a","b.md","deadbeef","file","file"));
    let v=lexical_hash_512("language tools Duolingo");
    assert_eq!(v.len(),512);
    let norm=v.iter().map(|x|x*x).sum::<f32>().sqrt();
    assert!((norm-1.0).abs()<1e-5);
}
#[test]
fn fail_closed_when_source_unreadable(){
    let tmp=tempfile::tempdir().unwrap();
    assert!(scan_directory(&tmp.path().join("missing"),"repo:x").is_err());
}

#[test]
fn code_native_parser_and_structural_graph() {
    let tmp=tempfile::tempdir().unwrap();
    fs::write(tmp.path().join("app.py"),"def greet(name):\n    return name\n").unwrap();
    fs::write(tmp.path().join("engine.rs"),"fn run() -> u32 { 42 }\n").unwrap();
    fs::write(tmp.path().join("model.ts"),"function calculate(x: number) { return x * 2; }\n").unwrap();
    let scan=scan_directory(tmp.path(),"repo:code-fixture").unwrap();
    verify_scan(&scan).unwrap();
    assert_eq!(scan.files_seen,3);
    for (path,kind) in [("app.py","function_definition"),
                        ("engine.rs","function_item"),
                        ("model.ts","function_declaration")] {
        let file=scan.records.iter().find(|r|r.source["key"]==path && r.kind=="file").unwrap();
        let nodes=file.native["nodes"].as_array().unwrap();
        assert!(!nodes.is_empty(),"native AST is required for {path}");
        assert_eq!(file.native["has_error"],false);
        assert!(nodes.iter().any(|n|n["kind"]==kind),"native {kind} missing from {path}");
        let symbol=scan.records.iter().find(|r|r.source["key"]==path && r.kind==kind).unwrap();
        assert_eq!(symbol.location["unit"],"utf8_byte");
        assert!(scan.edges.iter().any(|e|e.to==symbol.id && e.relation=="contains"));
    }
}
