"""Regression checks for the ten convenience views and open graph derivation."""
import unittest
import networkx as nx
from knowledge_positions import KnowledgePositions


class Encoder:
    def encode(self, text, normalize_embeddings=True):
        return [1.0, 0.0]


class TestGraphViews(unittest.TestCase):
    def setUp(self):
        self.k = KnowledgePositions("test", Encoder())
        self.a = self.k.add("a", "a", version="v1", position={"line": 1})
        self.b = self.k.add("b", "b", version="v1", position={"line": 1})
        self.c = self.k.add("c", "c", version="v1", position={"line": 1},
                            defer_embedding=True)
        # The two qualified parallel edges retain distinct evidence.
        self.k.link(self.b, self.a, "requires", evidence={"source": "a"}, cost=2)
        self.k.link(self.b, self.a, "related_to", evidence={"source": "b"}, cost=3)
        self.k.link(self.c, self.b, "requires", cost=1)

    def test_views_and_algorithms(self):
        before = list(self.k.graph.edges(keys=True, data=True))
        views = {}
        for kind in self.k.GRAPH_VIEWS:
            opts = {"root": self.a} if kind in ("tree", "neighborhood") else {}
            views[kind] = self.k.graph_view(kind, name="test-" + kind, **opts)
            self.assertEqual(views[kind].graph["name"], "test-" + kind)
        self.assertEqual(len(views), 10)
        self.assertTrue(nx.is_tree(views["tree"]))
        self.assertTrue(nx.is_forest(views["forest"]))
        self.assertTrue(nx.is_directed_acyclic_graph(views["dag"]))
        self.assertTrue(nx.is_bipartite(views["bipartite"]))
        self.assertEqual(views["weighted"][self.a][self.b]["cost"], 2)
        self.assertEqual(len(views["directed"][self.b][self.a]["original_edges"]), 2)
        # A deferred vector remains a graph node, with no invented similarity.
        self.assertEqual(views["similarity"].degree(self.c), 0)
        self.assertIsNone(self.k.graph.nodes[self.c]["vector"])
        result = self.k.core_algorithms(self.a, self.c)
        self.assertEqual(len(result["views"]), 10)
        self.assertEqual(result["topological_sort"], [self.a, self.b, self.c])
        self.assertEqual(result["shortest_path"], [self.a, self.b, self.c])
        self.assertEqual(before, list(self.k.graph.edges(keys=True, data=True)))

    def test_open_derivation_and_detachment(self):
        v = self.k.derive_graph("line-graph", nx.line_graph, source="directed")
        self.assertEqual(v.graph["name"], "line-graph")
        self.assertEqual(len(v), 2)
        # Editing a detached view must not edit stored source-backed data.
        v = self.k.graph_view("multigraph")
        v.nodes[self.a]["position"]["line"] = 99
        self.assertEqual(self.k.graph.nodes[self.a]["position"]["line"], 1)

    def test_cycle_and_cost_boundaries(self):
        self.k.link(self.a, self.c, "requires")
        with self.assertRaises(nx.NetworkXUnfeasible):
            self.k.graph_view("dag")
        with self.assertRaises(ValueError):
            self.k.graph_view("weighted")
        self.assertIsNone(self.k.core_algorithms(self.a, self.c)["topological_sort"])
        # Condensation produces an acyclic mathematical view, not false precedence.
        self.assertTrue(nx.is_directed_acyclic_graph(
            self.k.derive_graph("condensation", nx.condensation, source="directed")))

if __name__ == "__main__":
    unittest.main()
