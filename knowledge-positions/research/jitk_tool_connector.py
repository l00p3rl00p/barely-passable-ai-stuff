"""JITK tool connection: one small boundary, existing knowledge operations.

Receive a structured tool invocation and dispatch only approved read-only
JITK operations. The knowledge index, source files, search, and graph remain
owned by jit_index.py. This connector neither reindexes nor mutates knowledge.

Usage:
    echo '{"tool":"jitk.search","arguments":{"query":"context"}}' | python jitk_tool_connector.py
"""
from __future__ import annotations

import json
import sys

import jit_index


def connect(request: dict) -> dict:
    """Connect a named tool request to an existing JITK operation and return its result."""
    if not isinstance(request, dict):
        raise ValueError("request must be an object")
    tool = request.get("tool")
    args = request.get("arguments", {})
    if not isinstance(args, dict):
        raise ValueError("arguments must be an object")
    if tool == "jitk.search":
        if set(args) - {"query", "limit"}:
            raise ValueError("unsupported search argument")
        query = args.get("query")
        limit = args.get("limit", 7)
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be nonempty text")
        if type(limit) is not int or not (1 <= limit <= 25):
            raise ValueError("limit must be an integer between 1 and 25")
        result = [
            {"score": score, "tag": tag, "heading": heading, "id": node_id}
            for score, tag, heading, node_id in jit_index.search(query, limit)
        ]
    elif tool in {"jitk.read", "jitk.neighbors"}:
        if set(args) != {"tag"}:
            raise ValueError("exactly one tag argument is required")
        tag = args["tag"]
        if not isinstance(tag, str) or not tag.startswith("EKC:") or len(tag) > 24:
            raise ValueError("invalid knowledge tag")
        result = jit_index.read(tag) if tool == "jitk.read" else jit_index.neighbors(tag)
    else:
        raise ValueError("unknown JITK tool")
    return {"ok": True, "tool": tool, "result": result}


def main() -> int:
    # Standard input/output is a tool transport, not a new knowledge storage layer.
    # The process can serve one request or a sequence of newline-delimited requests.
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
            response = connect(request)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            response = {"ok": False, "error": str(exc)}
        print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
