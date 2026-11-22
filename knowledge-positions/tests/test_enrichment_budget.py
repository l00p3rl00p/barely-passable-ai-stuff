"""Regression tests for the hard three-touch enrichment mutation budget."""
import tempfile
import unittest
from pathlib import Path
from knowledge_positions import KnowledgePositions

class TestEnrichmentBudget(unittest.TestCase):
    def setUp(self):
        self.k = KnowledgePositions('test')
        self.a = self.k.add('doc:a', 'alpha', version='v1',
                            position={'line': 1}, defer_embedding=True)
        self.b = self.k.add('doc:b', 'beta', version='v1',
                            position={'line': 1}, defer_embedding=True)

    def test_third_touch_freezes_payload_but_not_outward_links(self):
        self.assertEqual(self.k.enrichment_state(self.a)['touches'], 1)
        self.k.enrich_node(self.a, {'summary': 'second-pass'}, source_version='v1')
        state = self.k.enrich_node(self.a, {'context': 'third-pass'}, source_version='v1')
        self.assertEqual(state['touches'], 3)
        self.assertTrue(state['frozen'])
        with self.assertRaises(ValueError):
            self.k.enrich_node(self.a, {'overflow': True}, source_version='v1')
        # Freeze the payload, not graph growth.
        self.k.link(self.a, self.b, 'related_to', evidence='new context branches outward')
        self.assertTrue(self.k.graph.has_edge(self.a, self.b))

    def test_new_verified_source_version_starts_a_fresh_node_budget(self):
        newer = self.k.add('doc:a', 'alpha revised', version='v2',
                           position={'line': 1}, defer_embedding=True)
        self.assertNotEqual(newer, self.a)
        self.assertEqual(self.k.enrichment_state(newer)['touches'], 1)
        self.assertFalse(self.k.enrichment_state(newer)['frozen'])

    def test_cluster_budget_freezes_and_resets_on_source_version_change(self):
        k = KnowledgePositions('test')
        a = k.add('cluster-source', 'one', version='v1', position={'line':1},
                  defer_embedding=True, cluster_id='topic')
        b = k.add('other-source', 'two', version='v1', position={'line':1},
                  defer_embedding=True, cluster_id='topic')
        self.assertEqual(k.enrichment_state(a, cluster_id='topic')['touches'], 1)
        k.enrich_node(a, {'pass': 2}, cluster_id='topic')
        state = k.enrich_node(b, {'pass': 3}, cluster_id='topic')
        self.assertTrue(state['frozen'])
        with self.assertRaises(ValueError):
            k.enrich_node(a, {'pass': 4}, cluster_id='topic')
        # Explicit new source content/version re-opens the cluster epoch.
        newer = k.add('cluster-source', 'one revised', version='v2',
                      position={'line':1}, defer_embedding=True, cluster_id='topic')
        state = k.enrichment_state(newer, cluster_id='topic')
        self.assertEqual(state['touches'], 1)
        self.assertFalse(state['frozen'])


    def test_cluster_budget_survives_save_and_reload(self):
        k = KnowledgePositions('test')
        a = k.add('cluster-source', 'one', version='v1', position={'line':1},
                  defer_embedding=True, cluster_id='topic')
        b = k.add('other-source', 'two', version='v1', position={'line':1},
                  defer_embedding=True, cluster_id='topic')
        k.enrich_node(a, {'pass': 2}, cluster_id='topic')
        k.enrich_node(b, {'pass': 3}, cluster_id='topic')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'graph.json'
            k.save(path)
            loaded = KnowledgePositions.load(path)
            state = loaded.enrichment_state(a, cluster_id='topic')
            self.assertEqual(state['touches'], 3)
            self.assertTrue(state['frozen'])
            with self.assertRaises(ValueError):
                loaded.enrich_node(a, {'overflow': True}, cluster_id='topic')

if __name__ == '__main__':
    unittest.main()
