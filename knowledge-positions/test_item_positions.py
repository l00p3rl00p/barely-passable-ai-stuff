"""Tests for source-relative structural locations, without requiring AST elsewhere."""
import ast
import hashlib
import tempfile
import unittest
from pathlib import Path

from knowledge_positions import KnowledgePositions


class Encoder:
    def __init__(self):
        self.calls = 0

    def encode(self, text, normalize_embeddings=True):
        self.calls += 1
        return [1.0, 0.0]


class TestItemPositions(unittest.TestCase):
    def test_ast_traversal_tags_real_paths_and_reuses_existing_vectors(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'sample.py'
            p.write_text('def example(x):\n    if x:\n        return x\n    return 0\n')
            enc = Encoder()
            k = KnowledgePositions('test', enc)
            first = k.ingest_python(p)
            vector_calls = enc.calls
            self.assertGreater(len(first), 2)
            self.assertEqual(len(first), len(set(first)))
            fn_id = next(n for n in first if k.graph.nodes[n]['kind'] == 'FunctionDef')
            loc = k.graph.nodes[fn_id]['item_location']
            self.assertEqual(loc['path'], ['Module', 'body[0]:FunctionDef'])
            self.assertEqual(loc['parent_path'], ['Module'])
            self.assertEqual(loc['sibling_index'], 0)
            self.assertEqual(loc['depth'], 1)
            self.assertEqual(loc['basis'], 'parser')
            self.assertEqual(loc['precision'], 'parsed')
            self.assertEqual(loc['source_version'], hashlib.sha256(p.read_bytes()).hexdigest())
            returned = [n for n in first if k.graph.nodes[n]['kind'] == 'Return']
            self.assertEqual(len(returned), 2)
            self.assertNotEqual(k.graph.nodes[returned[0]]['item_location']['path'],
                                k.graph.nodes[returned[1]]['item_location']['path'])
            before = len(k.graph)
            self.assertEqual(k.ingest_python(p), first)
            self.assertEqual(len(k.graph), before)
            self.assertEqual(enc.calls, vector_calls)
            self.assertFalse(k.record_item_position(
                fn_id, path=loc['path'], basis='parser', precision='parsed',
                sibling_index=0, source_version=loc['source_version']))
            original = ast.get_source_segment(p.read_text(), ast.parse(p.read_text()).body[0])
            enriched = k.positioned_embedding_input(fn_id, original)
            self.assertIn('Position within source: Module > body[0]:FunctionDef', enriched)
            self.assertIn('Original text:', enriched)
            self.assertEqual(enc.calls, vector_calls)
            with self.assertRaises(ValueError):
                k.positioned_embedding_input(fn_id, 'not the original function')
            saved = Path(td) / 'knowledge.json'
            k.save(saved)
            restored = KnowledgePositions.load(saved, Encoder())
            self.assertEqual(restored.graph.nodes[fn_id]['item_location'], loc)

    def test_structural_only_python_read_never_embeds(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'source.py'
            path.write_text('def f(x):\n    return x + 1\n')
            enc = Encoder()
            k = KnowledgePositions('test', enc)
            ids = k.ingest_python(path, defer_embedding=True)
            self.assertGreater(len(ids), 1)
            self.assertEqual(enc.calls, 0)
            self.assertTrue(all(k.graph.nodes[n]['vector'] is None for n in ids))
            self.assertTrue(all(k.graph.nodes[n]['item_location']['basis'] == 'parser'
                                for n in ids))
            self.assertEqual(k.ingest_python(path, defer_embedding=True), ids)
            self.assertEqual(enc.calls, 0)

    def test_line_only_and_anchor_coordinates_need_no_invented_tree(self):
        k = KnowledgePositions('test')
        nid = k.add('source', 'a section', version='v1', position={'line': 4},
                    defer_embedding=True)
        self.assertTrue(k.record_item_position(
            nid, basis='reader', precision='parsed',
            coordinates={'start_line': 4, 'end_line': 7}))
        loc = k.graph.nodes[nid]['item_location']
        self.assertIsNone(loc['path'])
        self.assertEqual(loc['method'], 'source_span')
        self.assertEqual(loc['coordinates']['start_line'], 4)
        self.assertIn('"start_line": 4', k.positioned_embedding_input(nid, 'a section'))
        self.assertTrue(k.record_item_position(
            nid, basis='reader', precision='parsed',
            coordinates={'anchor': 'sec-intro', 'start_line': 4}))
        self.assertEqual(k.graph.nodes[nid]['item_location']['method'], 'stable_anchor')
        self.assertEqual(k.graph.nodes[nid]['item_location']['coordinates']['end_line'], 7)
        # Better verified native structure supersedes method preference,
        # while secondary line/anchor coordinates remain useful.
        self.assertTrue(k.record_item_position(
            nid, basis='parser', precision='parsed',
            path=['document', 'sections[0]'],
            coordinates={'start_line': 4}))
        loc = k.graph.nodes[nid]['item_location']
        self.assertEqual(loc['method'], 'native_structure')
        self.assertEqual(loc['coordinates']['anchor'], 'sec-intro')
        self.assertEqual(loc['coordinates']['end_line'], 7)
        self.assertFalse(k.record_item_position(
            nid, basis='reader', precision='parsed',
            coordinates={'start_line': 4, 'end_line': 7}))
        self.assertEqual(k.graph.nodes[nid]['item_location']['method'], 'native_structure')
        with self.assertRaises(ValueError):
            k.record_item_position(
                nid, basis='parser', precision='parsed',
                path=['document', 'sections[1]'])
        with self.assertRaises(ValueError):
            k.record_item_position(
                nid, basis='reader', precision='parsed',
                coordinates={'start_line': 17})

    def test_novel_locator_convention_is_provisional_and_persistent(self):
        k = KnowledgePositions('test')
        self.assertEqual(k.location_method_catalog()['preferred'],
                         ['native_structure', 'stable_anchor',
                          'source_span', 'observed_locator'])
        self.assertTrue(k.register_location_method(
            'custom:layout-grid', source_kind='visual-page',
            description='Region marker using a reproducible layout grid.',
            verification='Reopen source revision and compare coordinates.'))
        self.assertFalse(k.register_location_method(
            'custom:layout-grid', source_kind='visual-page',
            description='Region marker using a reproducible layout grid.',
            verification='Reopen source revision and compare coordinates.'))
        nid = k.add('visual-page', 'caption', version='observed',
                    position={'selector': 'top-left'}, defer_embedding=True)
        self.assertTrue(k.record_item_position(
            nid, coordinates={'region': 'top-left'},
            method='custom:layout-grid', basis='observation'))
        with self.assertRaises(ValueError):
            k.record_item_position(
                nid, coordinates={'region': 'top-left'},
                method='custom:layout-grid', basis='parser', precision='parsed')
        with self.assertRaises(ValueError):
            k.register_location_method(
                'custom:layout-grid', source_kind='visual-page',
                description='Conflicting new schema.', verification='Another rule.')
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / 'g.json'
            k.save(db)
            restored = KnowledgePositions.load(db)
            self.assertEqual(restored.location_method_catalog(),
                             k.location_method_catalog())
            self.assertEqual(restored.graph.nodes[nid]['item_location']['method'],
                             'custom:layout-grid')

    def test_model_observation_is_a_lead_not_parser_verified(self):
        k = KnowledgePositions('test')
        nid = k.add('https://example.org/article', 'The fourth paragraph', version='observed-v1',
                    position={'selector': 'paragraph[3]'}, kind='paragraph',
                    defer_embedding=True)
        self.assertTrue(k.record_item_position(
            nid, path=['document', 'article', 'paragraph[3]'],
            basis='observation', sibling_index=3))
        loc = k.graph.nodes[nid]['item_location']
        self.assertEqual(loc['precision'], 'locator_only')
        self.assertEqual(loc['basis'], 'observation')
        self.assertEqual(loc['sibling_index'], 3)
        self.assertIsNone(k.graph.nodes[nid]['vector'])
        with self.assertRaises(ValueError):
            k.record_item_position(nid, path=['document'], basis='observation',
                                   precision='parsed')
        with self.assertRaises(ValueError):
            k.record_item_position(nid, path=['document'], basis='parser',
                                   precision='parsed', source_version='another-version')
        with self.assertRaises(ValueError):
            k.record_item_position(nid, path=[], basis='observation')
        with self.assertRaises(ValueError):
            k.record_item_position(nid, path=['document'], basis='observation',
                                   sibling_index=-1)

    def test_parser_metadata_cannot_be_downgraded_by_an_observation(self):
        k = KnowledgePositions('test')
        nid = k.add('source', 'known', version='v1', position={'line': 1},
                    defer_embedding=True)
        self.assertTrue(k.record_item_position(nid, path=['root', 'item[0]'],
                                                basis='parser', precision='parsed'))
        verified = dict(k.graph.nodes[nid]['item_location'])
        self.assertFalse(k.record_item_position(nid, path=['some guessed section'],
                                                 basis='observation'))
        self.assertEqual(k.graph.nodes[nid]['item_location'], verified)


if __name__ == '__main__':
    unittest.main()
