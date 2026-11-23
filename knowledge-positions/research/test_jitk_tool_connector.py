"""Exercise the actual current JITK index and original paper through one tool boundary."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

import jit_index
from jitk_tool_connector import connect

HERE = Path(__file__).resolve().parent


class JITKConnectorTests(unittest.TestCase):
    def test_real_search_read_and_relationships(self):
        # The existing JITK index verifies exact hashes against the original paper.
        index, _ = jit_index.load_verified()
        self.assertGreater(len(index["nodes"]), 0)
        term = index["nodes"][0]["heading"]
        results = connect({"tool": "jitk.search", "arguments": {"query": term, "limit": 5}})
        self.assertTrue(results["ok"])
        self.assertTrue(results["result"])
        found = results["result"][0]["tag"]
        paper_text = connect({"tool": "jitk.read", "arguments": {"tag": found}})
        self.assertIn(found, paper_text["result"])
        links = connect({"tool": "jitk.neighbors", "arguments": {"tag": found}})
        self.assertEqual(links["result"], jit_index.neighbors(found))

    def test_actual_stdio_tool_boundary(self):
        request = {"tool": "jitk.search", "arguments": {"query": "context", "limit": 2}}
        p = subprocess.run(
            [sys.executable, str(HERE / "jitk_tool_connector.py")],
            input=json.dumps(request) + "\n",
            capture_output=True, text=True, check=True, cwd=HERE,
        )
        response = json.loads(p.stdout)
        self.assertTrue(response["ok"])
        self.assertEqual(response["tool"], "jitk.search")
        self.assertLessEqual(len(response["result"]), 2)

    def test_explicit_allowlist(self):
        with self.assertRaisesRegex(ValueError, "unknown JITK tool"):
            connect({"tool": "jitk.delete", "arguments": {}})
        with self.assertRaisesRegex(ValueError, "unsupported search argument"):
            connect({"tool": "jitk.search", "arguments": {"query": "a", "path": "/etc/passwd"}})


if __name__ == "__main__":
    unittest.main()
