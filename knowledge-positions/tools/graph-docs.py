#!/usr/bin/env python3
"""Scan native Markdown into a navigable knowledge graph; no LLM or record copies."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

from markdown_it import MarkdownIt
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
INDEX = "index.md"
PARSER = MarkdownIt("commonmark", {"html": True})

def scan(root):
    """Return source document locations and observed directed hyperlinks."""
    root = root.resolve()
    docs, edges, warnings = {}, set(), []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if path.is_symlink() or any(p.startswith(".") for p in rel.parts) or rel.as_posix() == INDEX:
            continue
        name = rel.as_posix()
        raw = path.read_bytes()
        body = raw.decode("utf-8")
        if body.startswith(("---\n", "---\r\n")):
            lines = body.splitlines(keepends=True)
            end = next((i for i, line in enumerate(lines[1:], 1)
                        if line.rstrip("\r\n") == "---"), None)
            if end is not None:
                try:
                    fm = YAML(typ="safe").load("".join(lines[1:end]))
                    if not isinstance(fm, dict):
                        warnings.append(f"{name}: frontmatter is not a mapping")
                except Exception as exc:
                    warnings.append(f"{name}: invalid existing YAML ({type(exc).__name__})")
                body = "".join(lines[end+1:])
            else:
                warnings.append(f"{name}: unclosed frontmatter")
        tokens = PARSER.parse(body)
        headings, links = [], []
        for i, tok in enumerate(tokens):
            if tok.type == "heading_open" and i+1 < len(tokens):
                headings.append(tokens[i+1].content.strip())
            if tok.type == "inline":
                for child in tok.children or []:
                    if child.type == "link_open":
                        links.append(child.attrGet("href"))
        docs[name] = {"title": headings[0] if headings else path.stem,
                      "sha256": hashlib.sha256(raw).hexdigest(),
                      "headings": headings, "links": links}
    for source, doc in docs.items():
        for link in doc["links"]:
            if not link:
                continue
            uri = urlsplit(link)
            if uri.scheme or uri.netloc:
                continue
            target_path = unquote(uri.path)
            base = root if target_path.startswith("/") else (root / source).parent
            target = (base / target_path.lstrip("/")).resolve() if target_path else root / source
            try:
                name = target.relative_to(root).as_posix()
            except ValueError:
                continue
            if name in docs and name != source:
                edges.add((source, name, uri.fragment))
            elif name != INDEX and not target.exists():
                warnings.append(f"{source}: unresolved local link {link}")
    return docs, sorted(edges), warnings

def render(docs, edges):
    """One generated wiki-style directory; original files remain the entities."""
    incoming = {name: set() for name in docs}
    outgoing = {name: set() for name in docs}
    for source, target, _ in edges:
        incoming[target].add(source)
        outgoing[source].add(target)
    def link(name):
        title = docs[name]["title"].replace("[", r"\[").replace("]", r"\]").replace("|", r"\|")
        return f"[{title}]({quote(name, safe='/')})"
    lines = ["# Knowledge Positions — documentation knowledge graph", "",
             "This is the generated navigation view of the source documents, not a separate knowledge record store.",
             "Each document is its own entity; Markdown links are observed directed relationships. Folder membership is structural, not semantic.",
             "Open the existing [human guide](README.md) or [SDF assembly guide](SDF/README.md).",
             "", f"**{len(docs)} source documents · {len(set((s,t) for s,t,_ in edges))} directed document links**",
             "", "## Browse by area", ""]
    node_ids = {name: f"node-{i:03d}" for i, name in enumerate(docs, 1)}
    groups = {}
    for name in docs:
        group = name.rsplit("/", 1)[0] if "/" in name else "Overview"
        groups.setdefault(group, []).append(name)
    for group in sorted(groups, key=lambda g: (g != "Overview", g.lower())):
        lines.extend([f"### {group}", "", "| Source document | Links to | Linked from |", "|---|---:|---:|"])
        for name in groups[group]:
            lines.append(f"| {link(name)} | [{len(outgoing[name])}](#{node_ids[name]}) | [{len(incoming[name])}](#{node_ids[name]}) |")
        lines.append("")
    lines.extend(["## Relationship browser", "",
                  "These are native links, not inferred semantic relationships. A backlink is a reverse view of an observed link, not a new source assertion.", ""])
    for name in docs:
        lines.extend([f"### {node_ids[name]}", "", f"**{link(name)}**", "",
                      "- Links to: " + (", ".join(link(n) for n in sorted(outgoing[name])) or "—"),
                      "- Linked from: " + (", ".join(link(n) for n in sorted(incoming[name])) or "—"), ""])
    return "\n".join(lines).rstrip() + "\n"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="update generated index.md only")
    parser.add_argument("--graph-json", type=Path, help="optional derived graph for another tool (not an authoritative store)")
    args = parser.parse_args()
    docs, edges, warnings = scan(ROOT)
    content = render(docs, edges).encode("utf-8")
    index = ROOT / INDEX
    changed = not index.exists() or index.read_bytes() != content
    if args.write and changed:
        index.write_bytes(content)
    if args.graph_json:
        # Never write over an authoritative source.
        destination = args.graph_json.resolve()
        if destination == ROOT or ROOT in destination.parents:
            parser.error("--graph-json must be outside the source documentation area")
        destination.write_text(json.dumps({"documents": docs, "relationships": [
            {"source": s, "target": t, "fragment": f, "type": "observed-link"} for s,t,f in edges],
            "warnings": warnings}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"documents": len(docs), "directed_document_links": len(set((s,t) for s,t,_ in edges)),
                      "distinct_link_targets_including_fragments": len(edges),
                      "index_changed": changed, "existing_source_warnings": warnings}, indent=2))
    return int(changed and not args.write)

if __name__ == "__main__":
    raise SystemExit(main())
