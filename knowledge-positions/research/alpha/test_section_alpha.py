"""Alpha: real Markdown AST, OKF 0.2, incremental per-section change."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import networkx as nx
import yaml
from knowledge_positions import KnowledgePositions
from section_alpha import build, source_sections

HERE=Path(__file__).parent


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


class SectionAlphaTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.source=self.root/'paper.md';self.source.write_bytes((HERE/'fixture/paper.md').read_bytes())
        self.notes=self.root/'notes.yaml';self.notes.write_bytes((HERE/'notes.yaml').read_bytes())
        self.out=self.root/'out'

    def run_build(self, changed=None):return build(self.source,self.notes,self.out,changed)

    def graph(self):return KnowledgePositions.load(self.out/'graph.json')

    def test_first_admission_is_real_ast_and_okf(self):
        report=self.run_build()
        self.assertEqual(report['added'],['EKC:27','EKC:28'])
        self.assertEqual(report['ast_regenerated'],['EKC:27','EKC:28'])
        self.assertEqual(report['nodes'],20)
        self.assertEqual(report['edges'],20)
        self.assertEqual(report['components'],1)
        g=self.graph().graph
        self.assertTrue(nx.has_path(g.to_undirected(),'paper.md#EKC:27','paper.md#EKC:28'))
        self.assertTrue(any(d['relation']=='AST_CHILD' for _,_,d in g.edges(data=True)))
        self.assertTrue(any(d['relation']=='related_to' for _,_,d in g.edges(data=True)))
        self.assertTrue(any(d.get('tags')==['enforcement','prompt-limitations'] for _,d in g.nodes(data=True)))
        for tag in ['27','28']:
            doc=(self.out/'okf'/f'EKC-{tag}.md').read_text()
            self.assertTrue(doc.startswith('---\n'))
            meta=yaml.safe_load(doc.split('---\n',2)[1])
            self.assertEqual(meta['type'],'Research Section')
            original=(self.out/'okf'/meta['sources'][0]['resource']).resolve()
            self.assertEqual(original,self.source.resolve())
            self.assertEqual(meta['source_ref'],f'paper.md#EKC:{tag}')
            self.assertIn('knowledge_annotation_sha256',meta)
            ast=json.loads((self.out/'ast'/f'EKC-{tag}.json').read_text())
            self.assertEqual(ast['type'],'MarkdownSection')
            self.assertTrue(ast['children'])
            src=source_sections(self.source.read_bytes())[f'EKC:{tag}']
            self.assertEqual(meta['source_content_sha256'],hashlib.sha256(src['raw']).hexdigest())
            location=meta['x_jit_location']
            self.assertEqual(location['realm'],'local_file')
            self.assertEqual(location['source_id'],f'paper.md#EKC:{tag}')
            self.assertEqual(location['version_scope'],'section')
            self.assertEqual(location['source_version_sha256'],meta['source_content_sha256'])
            self.assertEqual(location['last_resolution'],'observed_read')
            self.assertEqual(location['position']['start_byte'],src['start_byte'])
            self.assertEqual(location['position']['end_byte'],src['end_byte'])
            self.assertEqual(location['position']['span_sha256'],meta['source_content_sha256'])
            self.assertEqual(location['position']['precision'],'verified_utf8_span')

    def test_no_op_does_not_rewrite_any_file(self):
        self.run_build(); files=list(self.out.rglob('*'))
        initial={p.relative_to(self.out): (digest(p),p.stat().st_mtime_ns) for p in files if p.is_file()}
        a=self.run_build(changed=['EKC:28'])
        self.assertEqual(a['unchanged'],['EKC:28'])
        self.assertEqual(a['ast_regenerated'],[])
        self.assertEqual(initial,{p.relative_to(self.out):(digest(p),p.stat().st_mtime_ns) for p in files if p.is_file()})

    def test_annotation_only_change_reuses_other_section_and_ast(self):
        self.run_build(); g0=self.graph().graph
        untouched={n:copy.deepcopy(dict(d)) for n,d in g0.nodes(data=True) if n=='paper.md#EKC:27' or d.get('owner_section')=='paper.md#EKC:27'}
        sha27=digest(self.out/'okf/EKC-27.md');sha28=digest(self.out/'okf/EKC-28.md');ast28=digest(self.out/'ast/EKC-28.json')
        before_content=g0.nodes['paper.md#EKC:28']['content_hash'];before_vector=g0.nodes['paper.md#EKC:28']['vector']
        y=yaml.safe_load(self.notes.read_text())
        y['sections']['EKC:28']['tags'].append('critical-runtime-boundary')
        self.notes.write_text(yaml.safe_dump(y))
        report=self.run_build(changed=['EKC:28'])
        self.assertEqual(report['knowledge_changed'],['EKC:28'])
        self.assertEqual(report['ast_regenerated'],[])
        self.assertEqual(digest(self.out/'okf/EKC-27.md'),sha27)
        self.assertNotEqual(digest(self.out/'okf/EKC-28.md'),sha28)
        self.assertEqual(digest(self.out/'ast/EKC-28.json'),ast28)
        g=self.graph().graph
        self.assertEqual(g.nodes['paper.md#EKC:28']['content_hash'],before_content)
        self.assertEqual(g.nodes['paper.md#EKC:28']['vector'],before_vector)
        self.assertEqual(untouched,{n:dict(g.nodes[n]) for n in untouched})

    def test_source_change_rebuilds_only_changed_section(self):
        self.run_build(); original27=digest(self.out/'ast/EKC-27.json')
        g0=self.graph().graph
        nodes27={n:copy.deepcopy(dict(d)) for n,d in g0.nodes(data=True) if n=='paper.md#EKC:27' or d.get('owner_section')=='paper.md#EKC:27'}
        before=g0.nodes['paper.md#EKC:28']['content_hash']
        data=self.source.read_text().replace('Longer prompts and agent instruction files can influence behavior', 'Prompts and agent instruction files can influence behavior')
        self.source.write_text(data)
        report=self.run_build(changed=['EKC:28'])
        self.assertEqual(report['source_changed'],['EKC:28'])
        self.assertEqual(report['ast_regenerated'],['EKC:28'])
        g=self.graph().graph
        self.assertNotEqual(g.nodes['paper.md#EKC:28']['content_hash'],before)
        self.assertEqual(nodes27,{n:dict(g.nodes[n]) for n in nodes27})
        self.assertEqual(digest(self.out/'ast/EKC-27.json'),original27)


if __name__=='__main__':unittest.main()
