"""Destination mappings, separate from the connector's transport."""
import json, urllib.parse
from connector import dumps, emit, http

NODE_FIELDS = frozenset("""id kind entity_type domain heading terms owner_namespace source_id
source_address source_repo source_commit source_path source_version_sha256 observed_source_version
source_precision position_unit start_byte end_byte start_line end_line position_coordinates
span_sha256 ownership realm possible_routes within_path sibling_index location_coordinates
location_method location_basis location_precision vector_lexical_hash_512_status
vector_lexical_hash_512 status status_history enrichment enrichment_touches
enrichment_touch_limit enrichment_frozen""".split())
EDGE_FIELDS=frozenset("relation evidence_key evidence qualification status origin confidence cost weight".split())

def validate(batch):
    nodes=batch["nodes"]; edges=batch.get("edges",[])
    if not isinstance(nodes,list) or not isinstance(edges,list): raise ValueError("Expected node/edge arrays")
    ids=set()
    for row in nodes:
        if set(row)-NODE_FIELDS: raise ValueError("Unknown knowledge node field")
        for k in ("id","kind","source_id","source_precision","status","enrichment_touches","enrichment_touch_limit","enrichment_frozen"):
            if k not in row or row[k] is None: raise ValueError("Required field: "+k)
        if row["id"] in ids: raise ValueError("Duplicate id")
        ids.add(row["id"])
        if row["status"]!="current" or row["enrichment_touches"]!=1 or row["enrichment_touch_limit"]!=3 or row["enrichment_frozen"] is not False:
            raise ValueError("Connector accepts new admissions only; lifecycle updates use canonical writer")
        if row["source_precision"] not in ("verified","locator_only"): raise ValueError("Unknown precision")
        v=row.get("vector_lexical_hash_512")
        if row.get("vector_lexical_hash_512_status")=="known" and (not isinstance(v,list) or len(v)!=512): raise ValueError("Invalid lexical vector")
        if row.get("vector_lexical_hash_512_status")!="known" and v is not None: raise ValueError("Unexpected vector")
    for e in edges:
        if set(e)-EDGE_FIELDS-{"from","to"} or not all(e.get(k) for k in ("from","to","relation","evidence_key","qualification")):
            raise ValueError("Invalid relationship")
    return nodes,edges

def omni(s,nodes,edges):
    # Append only: existing keys refuse rather than overwrite human enrichment.
    # Nodes then relationships in a single native batch; explicit limits.
    records=[{"type":"KnowledgeItem","data":n} for n in nodes]
    records += [{"edge":"Relationship","from":e["from"],"to":e["to"],"data":{k:v for k,v in e.items() if k not in ("from","to")}} for e in edges]
    body="".join(dumps(r)+"\n" for r in records)
    if len(body.encode())>8*1024*1024 or len(records)>5000: raise ValueError("Split at producer into bounded batches")
    url=s["base_url"].rstrip("/")+"/graphs/"+urllib.parse.quote(s["graph"],safe="")+"/load/ndjson?"+urllib.parse.urlencode({"branch":s["branch"],"mode":"append"})
    return emit({**s,"transport":"http","url":url,"ndjson":True},body)

def ladybug(s,nodes,edges):
    url=s["base_url"].rstrip("/")+"/cypher"
    def query(q,p): return http(url,{"query":q,"params":p},s.get("token_env"))
    # One Cypher statement per item with parameter binding. CREATE only; no
    # overwrite of existing records. Earlier confirmations survive a later failure.
    receipts=[]
    for row in nodes:
        keys=sorted(k for k,v in row.items() if v is not None)
        props=", ".join(k+": $"+k for k in keys)
        r=query("CREATE (k:KnowledgeItem {"+props+"}) RETURN k.id AS id",{k:row[k] for k in keys})
        if not r.get("rows"): raise RuntimeError("Node write was not confirmed")
        receipts.append(row["id"])
    for edge in edges:
        keys=sorted(k for k,v in edge.items() if k in EDGE_FIELDS and v is not None)
        props=", ".join(k+": $"+k for k in keys)
        r=query("MATCH (a:KnowledgeItem {id:$src}), (b:KnowledgeItem {id:$dst}) CREATE (a)-[r:Relationship {"+props+"}]->(b) RETURN r.evidence_key AS id",{"src":edge["from"],"dst":edge["to"],**{k:edge[k] for k in keys}})
        if not r.get("rows"): raise RuntimeError("Relationship endpoints absent or write unconfirmed")
        receipts.append(edge["evidence_key"])
    return {"confirmed":receipts}

def cbm(s,batch,nodes,edges):
    # Native extraction names must be provided by the producer; never invent QNs.
    native=batch["codebase_memory"]
    by_id={n["id"]:n for n in nodes}
    mapped=[]
    qns={}
    for n in native["nodes"]:
        kid=n["knowledge_id"]; row=by_id[kid]
        for k in ("label","name","qualified_name","file_path"): 
            if not isinstance(n.get(k),str) or not n[k]: raise ValueError("CBM native field missing: "+k)
        if n["qualified_name"] in qns.values(): raise ValueError("Duplicate CBM qualified name")
        qns[kid]=n["qualified_name"]
        props={**n.get("properties",{}),"knowledge_positions":row}
        mapped.append({**{k:n[k] for k in ("label","name","qualified_name","file_path")},"start_line":row.get("start_line") or 0,"end_line":row.get("end_line") or 0,"properties":dumps(props)})
    if set(qns)!=set(by_id): raise ValueError("CBM mapping missing knowledge nodes")
    native_edges=[]; seen=set()
    for e in edges:
        typ=native["relation_types"][e["relation"]]
        k=(qns[e["from"]],qns[e["to"]],typ)
        if k in seen: raise ValueError("CBM edge identity collision; preserve distinct evidence before emission")
        seen.add(k)
        native_edges.append({"src":k[0],"dst":k[1],"type":k[2],"properties":dumps({"knowledge_positions":e})})
    return emit({"transport":"command","argv":[s["binary"],"neuron-import",s["database"],s["project"],s["root"]]}, {"nodes":mapped,"edges":native_edges})

def map_and_emit(s,batch):
    if s["profile"]=="passthrough": return emit(s,batch)
    nodes,edges=validate(batch)
    if s["profile"]=="omnigraph": return omni(s,nodes,edges)
    if s["profile"]=="ladybug": return ladybug(s,nodes,edges)
    if s["profile"]=="codebase-memory": return cbm(s,batch,nodes,edges)
    raise ValueError("Unknown destination profile")
