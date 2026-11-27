import importlib.util
import tempfile
import unittest
from pathlib import Path

try:
    import markdown_it
    import ruamel.yaml
except ImportError:
    markdown_it = None

@unittest.skipIf(markdown_it is None, "documentation graph extras not installed")
class DocumentationGraphTest(unittest.TestCase):
    def test_native_links_and_source_preservation(self):
        script = Path(__file__).resolve().parents[1] / "tools" / "graph-docs.py"
        spec = importlib.util.spec_from_file_location("graph_docs", script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("# A\n\n[B][ref]\n\n[ref]: sub/b.md#heading\n\n```md\n[Fake](c.md)\n```\n\n[External](https://example.org/c.md)\n")
            (root / "sub").mkdir()
            (root / "sub/b.md").write_text("# B\n\n[A](/a.md)\n")
            (root / "c.md").write_text("# C\n")
            (root / "index.md").write_text("# Derived\n")
            before = {p: p.read_bytes() for p in root.rglob("*.md")}
            docs, edges, warnings = mod.scan(root)
            self.assertEqual(set(docs), {"a.md", "sub/b.md", "c.md"})
            self.assertEqual(edges, [("a.md", "sub/b.md", "heading"), ("sub/b.md", "a.md", "")])
            self.assertFalse(warnings)
            self.assertEqual(mod.render(docs, edges), mod.render(*mod.scan(root)[:2]))
            self.assertEqual(before, {p: p.read_bytes() for p in root.rglob("*.md")})
