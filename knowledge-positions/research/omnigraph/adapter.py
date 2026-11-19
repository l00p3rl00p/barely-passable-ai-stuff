"""Portable Knowledge Positions adapter. OmniGraph is the only graph store."""
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from knowledge_positions import KnowledgePositions
from encoder import ScannerLexicalEncoder, SPACE, _words, STOP

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def encode(text):
    return [float(x) for x in ScannerLexicalEncoder().encode(text)]

def library():
    return KnowledgePositions(SPACE, ScannerLexicalEncoder())

def source_row(path, domain=None, source_id=None, start=1, end=None, kind="text", heading=None):
    p = Path(path).resolve(strict=True)
    raw = p.read_bytes()
    lines = raw.splitlines(keepends=True)
    end = len(lines) if end is None else end
    if not 1 <= start <= end <= len(lines):
        raise ValueError("Invalid source line range")
    lo = sum(map(len, lines[:start-1]))
    hi = sum(map(len, lines[:end]))
    text = raw[lo:hi].decode("utf-8")
    pos = dict(unit="utf8_byte", start_byte=lo, end_byte=hi, start_line=start, end_line=end)
    source = source_id or p.as_uri()
    k = library()
    kid = k.add(source, text, version=digest(raw), position=pos, kind=kind)
    k.record_item_position(kid, basis="reader", precision="parsed",
                           coordinates={"start_byte":lo,"end_byte":hi}, source_version=digest(raw))
    n = k.graph.nodes[kid]
    loc = n["item_location"]
    row = dict(id=kid,kind=kind,entity_type=n["entity_type"],domain=domain,
               heading=heading or p.name,terms=" ".join(w for w in _words(text.lower()) if w not in STOP),
               owner_namespace=source,source_id=source,source_address=p.as_uri(),
               source_path=str(p), source_version_sha256=n["version"],source_precision="verified",
               position_unit=pos["unit"],start_byte=lo,end_byte=hi,start_line=start,end_line=end,
               span_sha256=n["content_hash"],realm="local_file",
               possible_routes=json.dumps([{"via":"local_file","locator":p.as_uri()}]),
               location_method=loc["method"],location_basis=loc["basis"],
               location_precision=loc["precision"],location_coordinates=json.dumps(loc["coordinates"]),
               vector_lexical_hash_512_status=n["vector_status"],vector_lexical_hash_512=n["vector"],
               status=n["status"],enrichment_touches=n["enrichment_touches"],
               enrichment_touch_limit=n["enrichment_touch_limit"],enrichment_frozen=n["enrichment_frozen"])
    return {key:value for key,value in row.items() if value is not None}

class Store:
    def __init__(self,target,graph=None,branch="main"):
        self.flags=["--target",target,"--branch",branch]
        if graph: self.flags += ["--graph",graph]
    def call(self,*args):
        out=subprocess.run(["omnigraph",*args,*self.flags,"--json"],capture_output=True,text=True)
        if out.returncode:
            raise RuntimeError(f"OmniGraph exit {out.returncode}; inspect target before retrying: {out.stderr} {out.stdout}")
        return json.loads(out.stdout)
    def query(self,name,params):
        args=["query",name,"--params",json.dumps(params)]
        # Direct graph targets use this file; deployed server targets use stored queries.
        if "--graph" not in self.flags: args += ["--query",str(Path(__file__).resolve().parent/"queries"/"kp.gq")]
        result=self.call(*args)
        data=result.get("data",result)
        rows=data.get("rows") if isinstance(data,dict) else None
        if not isinstance(rows,list): raise RuntimeError("Unrecognized native query response; no write attempted")
        return [{key.split(".",1)[-1]:val for key,val in row.items()} for row in rows]
    def get(self,kid):
        rows=self.query("item_rows",{"ids":[kid]})
        if len(rows)>1: raise RuntimeError("Unexpected duplicate key")
        return {k:v for k,v in rows[0].items() if v is not None} if rows else None
    def write(self,record,mode="merge"):
        # Native CLI's input format, not a second data store. Remove immediately.
        with tempfile.TemporaryDirectory(prefix="kp-load-") as tmp:
            p=Path(tmp)/"record.ndjson"
            p.write_text(json.dumps(record,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
            return self.call("load","--data",str(p),"--mode",mode)

def hydrate(k,row):
    k.graph.add_node(row["id"], source=row["source_id"],version=row["source_version_sha256"],
       position={key:row[key] for key in ("start_byte","end_byte","start_line","end_line") if key in row},
       kind=row["kind"],content_hash=row["span_sha256"],status=row["status"],
       status_history=[json.loads(x) for x in row.get("status_history",[])],
       enrichment=json.loads(row.get("enrichment","{}")),enrichment_touches=row["enrichment_touches"],
       enrichment_touch_limit=row["enrichment_touch_limit"],enrichment_frozen=row["enrichment_frozen"],
       vector=row.get("vector_lexical_hash_512"),vector_status=row["vector_lexical_hash_512_status"],
       embedding_model=SPACE)

def verify_source(row):
    raw=Path(row["source_path"]).read_bytes()
    span=raw[row["start_byte"]:row["end_byte"]]
    if digest(raw)!=row["source_version_sha256"] or digest(span)!=row["span_sha256"]:
        raise ValueError("Source changed; do not use as current evidence")
    return span.decode("utf-8")

def capture(store,row):
    old=store.get(row["id"])
    if old:
        if any(old.get(x)!=row.get(x) for x in ("source_id","source_version_sha256","span_sha256","domain")):
            raise ValueError("Existing identity has different source or domain; inspect instead of overwriting")
        if old["status"]!="current": raise ValueError("Historical item; do not revive implicitly")
        return row["id"]
    store.write({"type":"KnowledgeItem","data":row},"append")
    return row["id"]

def link(store,a,b,relation,evidence):
    if not relation.strip() or not evidence.strip(): raise ValueError("Qualified evidence required")
    k=library()
    for kid in dict.fromkeys((a,b)):
        row=store.get(kid)
        if not row or row["status"]!="current": raise ValueError("Both endpoints must be current")
        verify_source(row)
        hydrate(k,row)
    ev={"reason":evidence}
    key=k.link(a,b,relation,evidence=ev,qualification="reviewed_by_contributor")
    return store.write({"edge":"Relationship","from":a,"to":b,
        "data":{"relation":relation,"evidence_key":key,"evidence":json.dumps(ev,sort_keys=True),
        "qualification":"reviewed_by_contributor","status":"proposed","origin":"contributor"}})

def enrich(store,kid,meaning):
    if not meaning.strip(): raise ValueError("Meaning must be nonempty")
    row=store.get(kid)
    if not row: raise KeyError(kid)
    verify_source(row)
    k=library();hydrate(k,row)
    if meaning in k.graph.nodes[kid]["enrichment"].values(): return {"unchanged":True}
    n=k.graph.nodes[kid]
    k.enrich_node(kid,{f"touch_{n['enrichment_touches']+1}":meaning},source_version=row["source_version_sha256"])
    row.update(enrichment=json.dumps(n["enrichment"],ensure_ascii=False),
               enrichment_touches=n["enrichment_touches"],enrichment_frozen=n["enrichment_frozen"])
    return store.write({"type":"KnowledgeItem","data":row})

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target",required=True)
    p.add_argument("--graph")
    p.add_argument("--branch",default="main")
    subs=p.add_subparsers(dest="cmd",required=True)
    c=subs.add_parser("capture");c.add_argument("path");c.add_argument("--domain");c.add_argument("--source-id")
    c.add_argument("--start",type=int,default=1);c.add_argument("--end",type=int)
    c.add_argument("--kind",default="text");c.add_argument("--heading");c.add_argument("--reviewed",action="store_true",required=True)
    for name in ("item","read","neighbors"):
        c=subs.add_parser(name);c.add_argument("id")
    c=subs.add_parser("search");c.add_argument("text")
    c=subs.add_parser("by-source");c.add_argument("source")
    c=subs.add_parser("link");c.add_argument("src");c.add_argument("dst");c.add_argument("relation");c.add_argument("evidence");c.add_argument("--reviewed",action="store_true",required=True)
    c=subs.add_parser("enrich");c.add_argument("id");c.add_argument("meaning");c.add_argument("--reviewed",action="store_true",required=True)
    a=p.parse_args();s=Store(a.target,a.graph,a.branch)
    if a.cmd=="capture": result=capture(s,source_row(a.path,a.domain,a.source_id,a.start,a.end,a.kind,a.heading))
    elif a.cmd=="search": result=s.query("search",{"vq":encode(a.text),"tq":a.text})
    elif a.cmd=="by-source": result=s.query("by_source",{"source":a.source})
    elif a.cmd=="item": result=s.get(a.id)
    elif a.cmd=="read":
        row=s.get(a.id)
        if not row: raise KeyError(a.id)
        if row["status"]!="current": raise ValueError("Historical item")
        result=verify_source(row)
    elif a.cmd=="neighbors": result={"out":s.query("out_rels",{"id":a.id}),"in":s.query("in_rels",{"id":a.id})}
    elif a.cmd=="link": result=link(s,a.src,a.dst,a.relation,a.evidence)
    else: result=enrich(s,a.id,a.meaning)
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__": main()
