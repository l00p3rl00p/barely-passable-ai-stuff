"""Regression tests for three-hop conversation lookup and cache invalidation."""
import unittest
from knowledge_positions import KnowledgePositions

class TestChatContext(unittest.TestCase):
    def setUp(self):
        self.k = KnowledgePositions('test')
        # Deferred vectors intentionally avoid any external model or download.
        self.ids = [self.k.add(f'chat:{i}', f'passage {i}', version='v1',
                               position={'line': 1}, defer_embedding=True)
                    for i in range(7)]
        for a,b in zip(self.ids,self.ids[1:]):
            self.k.link(b,a,'requires')

    def test_strict_depth_and_other(self):
        result = self.k.chat_context(self.ids[0], direction='in')
        self.assertEqual(result['levels'], [[n] for n in self.ids[:4]])
        self.assertEqual(set(result['nodes']), set(self.ids[:4]))
        self.assertEqual(len(result['edges']), 3)
        self.assertEqual(result['other']['label'], 'other')
        self.assertEqual(result['other']['count'], 1)
        self.assertEqual(result['other']['boundary_refs'][0]['node_id'], self.ids[4])
        self.assertNotIn(self.ids[5], str(result))
        self.assertEqual(len(self.k.graph_view('dag')), 7)
        # Cached results are detached from the caller.
        result['nodes'].clear()
        self.assertEqual(len(self.k.chat_context(self.ids[0], direction='in')['nodes']), 4)

    def test_write_and_cascade_invalidate(self):
        self.k.chat_context(self.ids[0], direction='in')
        self.assertTrue(self.k._chat_cache)
        self.k.link(self.ids[6], self.ids[0], 'related_to')
        self.assertFalse(self.k._chat_cache)
        self.assertIn(self.ids[6], self.k.chat_context(self.ids[0], direction='in')['nodes'])
        self.k.mark_source_changed('chat:0', 'v2')
        self.assertFalse(self.k._chat_cache)
        self.assertTrue(all(self.k.graph.nodes[n]['status'] == 'stale' for n in self.ids))
        with self.assertRaises(ValueError):
            self.k.chat_context(self.ids[0])

    def test_direction_and_filter(self):
        self.assertEqual(self.k.chat_context(self.ids[0], direction='out')['nodes'], [self.ids[0]])
        self.assertEqual(self.k.chat_context(self.ids[0], relations=['related_to'])['nodes'], [self.ids[0]])
        # Direct mutations remain available, with explicit cache invalidation.
        self.k.graph.add_edge(self.ids[0], self.ids[6], relation='related_to')
        self.k.invalidate_cache()
        self.assertIn(self.ids[6], self.k.chat_context(self.ids[0], relations=['related_to'])['nodes'])

if __name__ == '__main__':
    unittest.main()
