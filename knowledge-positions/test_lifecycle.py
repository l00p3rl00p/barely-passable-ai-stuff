import unittest, tempfile
from pathlib import Path
from knowledge_positions import KnowledgePositions

class Encoder:
    def encode(self, text, normalize_embeddings=True): return [1.,0.]

class TestLifecycle(unittest.TestCase):
    def setUp(self):
        self.k=KnowledgePositions("test",Encoder())
        self.ids={x:self.k.add(x,x,version="v1",position={"line":1}) for x in "abcde"}
        a,b,c,d,e=map(self.ids.get,"abcde")
        self.k.link(b,a,"derived_from")
        self.k.link(c,b,"depends_on")
        self.k.link(d,a,"shared_terms")

    def test_cascade(self):
        a,b,c,d,e=map(self.ids.get,"abcde")
        self.assertEqual(set(self.k.mark_source_changed("a","v2")),{a,b,c})
        self.assertEqual(self.k.graph.nodes[d]["status"],"current")
        self.assertEqual(self.k.graph.nodes[e]["status"],"current")
        self.assertEqual({n for n,_ in self.k.search("x")},{d,e})
        self.assertEqual(len(self.k.search("x",include_historical=True)),5)
        with self.assertRaises(ValueError): self.k.revalidate(c,"review")
        with self.assertRaises(ValueError): self.k.revalidate(a,"verified")
        new=self.k.add("a","a2",version="v2",position={"line":1})
        self.k.graph.remove_edge(b,a)
        self.k.link(b,new,"derived_from")
        self.k.revalidate(b,"verified")
        self.k.revalidate(c,"verified")
        self.assertEqual(len(self.k.search("x")),5)

    def test_deprecate(self):
        a,b,c,d,e=map(self.ids.get,"abcde")
        self.k.deprecate(a,"replaced",e)
        self.assertEqual(self.k.graph.nodes[a]["status"],"deprecated")
        self.assertEqual(self.k.graph.nodes[b]["status"],"stale")
        with self.assertRaises(ValueError): self.k.revalidate(a,"review")
        with tempfile.TemporaryDirectory() as p:
            self.k.save(Path(p)/"g.json")
            g=KnowledgePositions.load(Path(p)/"g.json",Encoder())
            self.assertEqual(g.graph.nodes[a]["status"],"deprecated")
            self.assertEqual(len(g.graph.nodes[a]["status_history"]),1)

    def test_cycle_and_late_dependency(self):
        a,b,c,d,e=map(self.ids.get,"abcde")
        self.k.link(a,c,"requires")
        self.k.invalidate(a,"changed")
        self.k.link(e,b,"derived_from")
        self.assertEqual(self.k.graph.nodes[e]["status"],"stale")
        self.assertEqual(self.k.graph.nodes[d]["status"],"current")
        self.assertEqual(self.k.graph.nodes[a]["status"],"stale")

if __name__=="__main__": unittest.main()
