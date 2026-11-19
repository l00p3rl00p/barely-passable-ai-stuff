import tempfile
import unittest
from pathlib import Path
from adapter import source_row, verify_source, library, hydrate, encode

class CaptureTests(unittest.TestCase):
    def test_positions_proximity_and_budget(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"actual.md"
            p.write_text("Alpha\nLego brick\n",encoding="utf-8")
            r=source_row(p,"books",start=2,end=2)
            self.assertEqual(r["id"],source_row(p,"books",start=2,end=2)["id"])
            self.assertEqual(verify_source(r),"Lego brick\n")
            self.assertEqual(r["start_byte"],6)
            self.assertEqual(r["vector_lexical_hash_512"],encode("Lego brick\n"))
            self.assertEqual(len(r["vector_lexical_hash_512"]),512)
            k=library();hydrate(k,r)
            k.enrich_node(r["id"],{"first":"one"})
            k.enrich_node(r["id"],{"second":"two"})
            with self.assertRaises(ValueError):k.enrich_node(r["id"],{"third":"three"})
            p.write_text("Changed\n",encoding="utf-8")
            with self.assertRaises(ValueError):verify_source(r)

if __name__=="__main__":unittest.main()
