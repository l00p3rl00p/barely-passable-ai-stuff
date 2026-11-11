#!/usr/bin/env python3
"""Incremental Markdown AST -> OKF v0.2 + Knowledge Positions alpha.

The ORIGINAL manuscript is read-only. Only selected EKC sections are refreshed.
Annotations are explicit caller inputs, never inferred from the parser; human review is not assumed.
Reuses stable section identities and unchanged AST/OKF files.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

import networkx as nx
import yaml
from markdown_it import MarkdownIt

for parent in Path(__file__).resolve().parents:
    if (parent / 'knowledge_positions.py').is_file():
        sys.path.insert(0, str(parent))
        break  # import the existing library beside the project, never replace it
from knowledge_positions import KnowledgePositions


def digest(raw):
    return hashlib.sha256(raw if isinstance(raw, bytes) else raw.encode('utf-8')).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()


class LexicalEncoder:
    """Deterministic explicit lexical vectors; never labeled semantic."""
    def encode(self, text, normalize_embeddings=True):
        import numpy as np
        v = np.zeros(512)
        for word in re.findall(r'\w+', text.lower()):
            h = hashlib.sha256(word.encode()).digest()
            v[int.from_bytes(h[:4], 'big') % 512] += 1 if h[4] & 1 else -1
        norm = np.linalg.norm(v)
        return v / norm if norm else v


def source_sections(raw):
    """Locate tagged sections from ACTUAL CommonMark heading tokens, not a regex over text."""
    text = raw.decode('utf-8')
    lines = text.splitlines(keepends=True)
    byte_offset = [0]
    for line in lines:
        byte_offset.append(byte_offset[-1] + len(line.encode()))
    tokens = MarkdownIt('commonmark', {'html': True}).parse(text)
    found = []
    for i, tok in enumerate(tokens[:-1]):
        if tok.type != 'heading_open' or tok.tag != 'h2' or not tok.map:
            continue
        heading = tokens[i+1].content if tokens[i+1].type == 'inline' else ''
        match = re.search(r'\[EKC:(\d{2})\]\s*$', heading)
        if match:
            found.append((f'EKC:{match.group(1)}', heading, tok.map[0]))
    out = {}
    for i, (tag, title, start) in enumerate(found):
        end = found[i+1][2] if i+1 < len(found) else len(lines)
        start_byte, end_byte = byte_offset[start], byte_offset[end]
        out[tag] = dict(tag=tag, title=title, start_line=start,
                        start_byte=start_byte, end_byte=end_byte,
                        raw=raw[start_byte:end_byte])
    return out


def syntax_ast(section):
    """Real token tree with nesting and absolute byte spans; no generated semantic claims."""
    raw = section['raw']
    text = raw.decode('utf-8')
    lines = text.splitlines(keepends=True)
    linebytes = [0]
    for l in lines:
        linebytes.append(linebytes[-1]+len(l.encode('utf-8')))
    root = dict(type='MarkdownSection', tag=section['tag'],
                start_byte=section['start_byte'], end_byte=section['end_byte'], children=[])
    stack = [root]
    serial = 0
    occurrences = Counter()
    def insert(tok, parent):
        nonlocal serial
        serial += 1
        pos = tok.map
        if pos:
            start = section['start_byte']+linebytes[pos[0]]
            end = section['start_byte']+linebytes[pos[1]]
            sub = raw[linebytes[pos[0]]:linebytes[pos[1]]]
            hash_value = digest(sub)
            position = {'start_byte':start,'end_byte':end,'unit':'utf8_byte','status':'exact_lines'}
        else:
            hash_value = digest(f'{tok.type}|{tok.content}|{tok.markup}')
            position = None  # inline children often have no exact independent offsets
        occurrences[(tok.type, hash_value)] += 1
        uid = f"paper.md#{section['tag']}/ast/{tok.type}/{hash_value[:20]}/{occurrences[(tok.type,hash_value)]}"
        item = dict(id=uid, type=tok.type, tag=tok.tag, nesting=tok.nesting,
                    markup=tok.markup, position=position, content_hash=hash_value,
                    attrs=dict(tok.attrs or {}), children=[])
        parent['children'].append(item)
        for child in tok.children or []:
            insert(child, item)
        return item
    for tok in MarkdownIt('commonmark', {'html': True}).parse(text):
        if tok.nesting == -1:
            if len(stack) <= 1:
                raise ValueError('Malformed markdown nesting')
            stack.pop()
            continue
        item = insert(tok, stack[-1])
        if tok.nesting == 1:
            stack.append(item)
    if len(stack) != 1:
        raise ValueError('Unclosed markdown constructs')
    graph_nodes = []
    def visit(node, nearest):
        for child in node['children']:
            if child['position'] is not None:
                graph_nodes.append((child['id'], child, nearest))
                visit(child, child['id'])
            else:
                visit(child, nearest)
    visit(root, f"paper.md#{section['tag']}")
    return root, graph_nodes


def annotate(section, ast_nodes, entry):
    """Validate caller-proposed paragraph notes against actual source spans."""
    allowed = {'summary','tags','relationships','paragraphs'}
    if set(entry) - allowed or not entry.get('summary') or not isinstance(entry.get('tags'),list):
        raise ValueError('Invalid annotation')
    paragraphs = []
    target_raw = section['raw']
    for note in entry.get('paragraphs', []):
        snippet = note.get('quote', '')
        if not snippet or target_raw.decode().count(snippet) != 1:
            raise ValueError('Paragraph quote is not a unique observed source snippet: ' + snippet[:70])
        # Choose the smallest actual PARAGRAPH token containing the exact quote.
        hits=[]
        for uid, tok, _ in ast_nodes:
            if tok['type']!='paragraph_open' or not tok['position']:
                continue
            pos=tok['position'];local=target_raw[pos['start_byte']-section['start_byte']:pos['end_byte']-section['start_byte']].decode()
            if snippet in local:hits.append((uid,tok))
        if len(hits)!=1:
            raise ValueError('Quoted paragraph does not uniquely resolve to a parser node: '+snippet[:70])
        uid,tok=hits[0]
        paragraphs.append(dict(id=uid, content_hash=tok['content_hash'],
                               quote=snippet, tags=note.get('tags',[]),
                               summary=note.get('summary',''),
                               relationships=note.get('relationships',[])))
    return {'summary':entry['summary'],'tags':entry['tags'],
            'relationships':entry.get('relationships',[]),'paragraphs':paragraphs}


def okf(section, annotations, content_hash, annotation_hash, source_resource):
    tag=section['tag']; slug=tag.replace(':','-')
    meta={'type':'Research Section','title':section['title'],
          'description':annotations['summary'],'tags':annotations['tags'],
          'status':'draft',
          'sources':[{'id':'manuscript','resource':source_resource, 'title':'Original research manuscript'}],
          'source_ref':f'paper.md#{tag}',
          'source_span':{'start_byte':section['start_byte'],'end_byte':section['end_byte'],'unit':'utf8_byte'},
          'source_content_sha256':content_hash,
          'knowledge_annotation_sha256':annotation_hash,
          'ast_ref':f'../ast/{slug}.json',
          # OKF v0.2 permits producer-defined metadata. This is an observed
          # local source read, NOT a public-access or cross-owner permission.
          'x_jit_location': {
              'owner_namespace': None,
              'realm': 'local_file',
              'source_id': f'paper.md#{tag}',
              'source_version_sha256': content_hash,
              'version_scope': 'section',
              'position': {
                  'start_byte': section['start_byte'],
                  'end_byte': section['end_byte'],
                  'unit': 'utf8_byte',
                  'span_sha256': content_hash,
                  'precision': 'verified_utf8_span'},
              'possible_routes': [{'environment': 'python_process', 'via': 'filesystem'}],
              'last_resolution': 'observed_read'}}
    lines=['# Summary','',annotations['summary'],'','## Annotated paragraphs','']
    for note in annotations['paragraphs']:
        lines.extend([f"- **{note['id']}**: {note['summary']} (tags: {', '.join(note['tags'])}; source hash: `{note['content_hash'][:16]}`)",''])
        for link in note['relationships']:
            lines.append(f"  - `{link['type']}` → [{link['target']}](./{link['target'].replace(':','-')}.md): {link['evidence']}")
    lines.extend(['## Relationships',''])
    for e in annotations['relationships']:
        t=e['target'];f=t.replace(':','-')
        lines.append(f"- `{e['type']}` → [{t}](./{f}.md): {e['evidence']}")
    if not annotations['relationships']:
        lines.append('- None established.')
    return '---\n'+yaml.safe_dump(meta,sort_keys=False,allow_unicode=True)+'---\n\n'+'\n'.join(lines)+'\n'


def build(source, notes, output, changed=None):
    raw=Path(source).read_bytes()
    sections=source_sections(raw)
    config=yaml.safe_load(Path(notes).read_text())['sections']
    if changed is None:
        requested=set(config)
    else:
        requested=set(changed)
    if requested-set(config):raise ValueError('No annotation supplied for: '+str(requested-set(config)))
    if requested-set(sections):raise ValueError('Source section not found: '+str(requested-set(sections)))
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    db=output/'graph.json'
    k=KnowledgePositions.load(db,LexicalEncoder()) if db.exists() else KnowledgePositions('lexical-hash-512',LexicalEncoder())
    report={'added':[], 'source_changed':[], 'knowledge_changed':[], 'unchanged':[], 'ast_regenerated':[], 'reused_nodes':0}
    for tag in sorted(requested):
        sec=sections[tag];sid=f'paper.md#{tag}'
        source_hash=digest(sec['raw'])
        old=k.graph.nodes[sid] if sid in k.graph else None
        # The source hash is determined only for requested sections, not for every section.
        ast_file=output/'ast'/f'{tag.replace(":","-")}.json'
        content_changed=old is None or old['content_hash']!=source_hash
        if content_changed:
            ast,nodes=syntax_ast(sec)
            annotations=annotate(sec,nodes,config[tag])
        else:
            ast=json.loads(ast_file.read_text())
            nodes=[]
            # Resolve selector from preserved AST, not a second parse of unchanged source.
            def walk(node,parent):
                for child in node['children']:
                    if child['position'] is not None:
                        nodes.append((child['id'],child,parent))
                        walk(child,child['id'])
                    else:
                        walk(child,parent)
            walk(ast,sid)
            annotations=annotate(sec,nodes,config[tag])
        annotation_hash=digest(canonical(annotations))
        original_knowledge=old.get('knowledge_hash') if old else None
        if old and not content_changed and original_knowledge==annotation_hash:
            report['unchanged'].append(tag);report['reused_nodes']+=len(nodes)+1
            continue
        if old is not None and content_changed:
            to_remove=[n for n,d in k.graph.nodes(data=True) if d.get('owner_section')==sid]
            k.graph.remove_nodes_from(to_remove)
            old['history']=old.get('history',[])+[{'content_hash':old['content_hash'],'knowledge_hash':old.get('knowledge_hash')}]
        if old is None:
            k.add('paper.md',sec['raw'].decode(),version=source_hash,
                  position={'start_byte':sec['start_byte'],'end_byte':sec['end_byte'],'unit':'utf8_byte'},
                  kind='MarkdownSection',node_id=sid)
            report['added'].append(tag)
        else:
            if content_changed:
                old['content_hash']=source_hash;old['version']=source_hash
                old['vector']=[float(v) for v in LexicalEncoder().encode(sec['raw'].decode())]
                report['source_changed'].append(tag)
            else:
                report['knowledge_changed'].append(tag)
            old['position']={'start_byte':sec['start_byte'],'end_byte':sec['end_byte'],'unit':'utf8_byte'}
        k.graph.nodes[sid].update(knowledge_hash=annotation_hash,source_ref=sid,
                                  tags=annotations['tags'], summary=annotations['summary'],
                                  annotation_status='proposed_from_config')
        if content_changed:
            for uid, token, parent in nodes:
                # Only source-addressable parser nodes become Knowledge Positions nodes.
                pos=token['position']
                raw_span=raw[pos['start_byte']:pos['end_byte']]
                k.add('paper.md',raw_span.decode(),version=digest(raw_span),
                      position=pos,kind='AST:'+token['type'],node_id=uid)
                k.graph.nodes[uid].update(owner_section=sid,ast_type=token['type'],
                                          ast_content_hash=token['content_hash'])
                k.link(parent,uid,'AST_CHILD',evidence={'origin':'markdown-it-py','qualification':'syntactic nesting, not inferred semantics'})
            ast_file.parent.mkdir(parents=True,exist_ok=True)
            ast_file.write_text(json.dumps(ast,ensure_ascii=False,indent=2)+'\n')
            report['ast_regenerated'].append(tag)
        # Paragraph knowledge is attached to the corresponding parser-derived node.
        for note in annotations['paragraphs']:
            node=k.graph.nodes[note['id']]
            node['tags']=note['tags']
            node['summary']=note['summary']
            node['knowledge_hash']=digest(canonical({k:v for k,v in note.items() if k!='id'}))
            for a,b,key,e in list(k.graph.out_edges(note['id'],keys=True,data=True)):
                if e.get('evidence',{}).get('origin')=='alpha_annotation_config':
                    k.graph.remove_edge(a,b,key)
            for link in note['relationships']:
                target=f"paper.md#{link['target']}"
                if target not in k.graph:raise ValueError('Paragraph relation target must already exist: '+target)
                k.link(note['id'],target,link['type'],
                       evidence={'origin':'alpha_annotation_config','qualification':link['evidence']})
        # Updating knowledge changes only section annotations. Preserve structural graph.
        for a,b,key,e in list(k.graph.edges(keys=True,data=True)):
            if a==sid and e.get('relation')=='related_to' and e.get('evidence',{}).get('origin')=='alpha_annotation_config':
                k.graph.remove_edge(a,b,key)
        for e in annotations['relationships']:
            if e['target'] not in config:
                raise ValueError('Relation target not in reviewed notes')
            target=f"paper.md#{e['target']}"
            if target not in k.graph:
                # Need the other node first; process both on initial invocation.
                raise ValueError('Target must already exist: '+target)
            k.link(sid,target,e['type'],evidence={'origin':'alpha_annotation_config','qualification':e['evidence']})
        f=output/'okf'/f'{tag.replace(":","-")}.md'
        f.parent.mkdir(parents=True,exist_ok=True)
        source_resource=Path(os.path.relpath(Path(source).resolve(), f.parent.resolve())).as_posix()
        f.write_text(okf(sec,annotations,source_hash,annotation_hash,source_resource),encoding='utf-8')
    k.invalidate_cache() if hasattr(k,'invalidate_cache') else None
    if report['added'] or report['source_changed'] or report['knowledge_changed']:
        k.save(db)
    # Count persisted structural knowledge; this is a real NetworkX graph.
    u=nx.Graph(k.graph)
    report.update(nodes=k.graph.number_of_nodes(),edges=k.graph.number_of_edges(),components=nx.number_connected_components(u))
    return report


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--notes',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--changed',action='append',help='Only inspect/re-hash this tagged section, e.g. EKC:28')
    a=p.parse_args()
    print(json.dumps(build(a.source,a.notes,a.output,a.changed),indent=2))

if __name__=='__main__':main()
