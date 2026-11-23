import argparse, hashlib, json, pathlib, re, sqlite3
import numpy as np
from knowledge_positions import KnowledgePositions
ROOT=pathlib.Path(__file__).parent
class LexicalEncoder:
    def encode(self,text,normalize_embeddings=True):
        a=np.zeros(512)
        for token in re.findall(r'\w+',text.lower()):
            h=hashlib.sha256(token.encode()).digest(); a[int.from_bytes(h[:4],'big')%512]+=1 if h[4]%2 else -1
        n=np.linalg.norm(a); return a/n if n else a

def encoder(model):
    return LexicalEncoder() if model=='lexical-hash-512' else None

def build(source,model):
    raw=source.read_bytes(); version=hashlib.sha256(raw).hexdigest(); k=KnowledgePositions(model,encoder(model)); prev=None; ids=[]
    db=sqlite3.connect(ROOT/'index.sqlite'); db.execute('DROP TABLE IF EXISTS search'); db.execute('DROP TABLE IF EXISTS refs'); db.execute("CREATE VIRTUAL TABLE search USING fts5(text, content='')"); db.execute('CREATE TABLE refs(rowid INTEGER PRIMARY KEY, node TEXT)')
    offset=0
    for line in raw.splitlines(keepends=True):
        text=line.decode('utf-8').strip(); end=offset+len(line.rstrip(b'\r\n'))
        if text:
            n=k.add(source.name,text,version=version,position={'start_byte':offset,'end_byte':end},kind='passage'); ids.append(n)
            if prev: k.link(prev,n,'next_passage')
            prev=n; row=len(ids); db.execute('INSERT INTO search(rowid,text) VALUES (?,?)',(row,text)); db.execute('INSERT INTO refs VALUES (?,?)',(row,n))
        offset+=len(line)
    terms=[set(re.findall(r'\w+',x.decode().lower()))-set('the a an of to it is in and that we you its for from be can our'.split()) for x in raw.splitlines() if x.strip()]
    for i,a in enumerate(terms):
        for j in range(i+1,len(terms)):
            b=terms[j]; common=a&b
            if len(common)>=2: k.link(ids[i],ids[j],'shared_terms',weight=len(common)/len(a|b))
    db.commit(); db.close(); k.save(ROOT/'index.json'); print(len(ids),'nodes',k.graph.number_of_edges(),'edges',version)

def load():
    p=ROOT/'index.json'; model=json.loads(p.read_text())['model']; return KnowledgePositions.load(p,encoder(model))
def read(k,n,source):
    d=k.graph.nodes[n]; raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=d['version']: raise ValueError('source changed')
    p=d['position']; b=raw[p['start_byte']:p['end_byte']]
    if hashlib.sha256(b.decode().strip().encode()).hexdigest()!=d['content_hash']: raise ValueError('span changed')
    return b.decode()
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['build','search','read','neighbors']); p.add_argument('value',nargs='?',default=''); p.add_argument('--source',type=pathlib.Path,default=ROOT/'source.txt'); p.add_argument('--model',default='lexical-hash-512'); a=p.parse_args()
    if a.action=='build': build(a.source,a.model)
    else:
        k=load()
        if a.action=='search':
            db=sqlite3.connect(ROOT/'index.sqlite'); terms=re.findall(r'\w+',a.value); exact=db.execute('SELECT refs.node FROM search JOIN refs ON search.rowid=refs.rowid WHERE search MATCH ? LIMIT 10',(' OR '.join('"'+t+'"' for t in terms),)).fetchall() if terms else []
            print(json.dumps({'exact':[x[0] for x in exact],'vector':k.search(a.value)},indent=2))
        elif a.action=='read': print(read(k,a.value,a.source))
        else: print(json.dumps(k.neighbors(a.value),indent=2))
