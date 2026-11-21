#!/usr/bin/env python3
"""Characterize ORIGINAL Scratchpad OpenKC with GPS-style fields.

Requires the original script from quatrus-scratchpad:
    experiments/openkc-ast-okf-yanp/openkc_etl.py

This does NOT reimplement/copy its conversion logic. It imports and calls the
original functions. Default mode checks the historically proven byte/AST
round trip and reports which literal fields were mapped to OKF metadata.
Use --require-field-crosswalk to test the stronger SDK behavior; against the
2026-11-03 original implementation this is expected to FAIL (exit 1).
"""
import argparse
import importlib.util
import json
from pathlib import Path

FIELDS = ("postal_code", "latitude", "longitude")


def load_original(path):
    spec = importlib.util.spec_from_file_location("original_openkc_etl", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load original OpenKC script")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--openkc-script", type=Path, required=True,
                    help="Actual quatrus-scratchpad/.../openkc_etl.py")
    ap.add_argument("--fixture", type=Path,
                    default=Path(__file__).resolve().parents[1] /
                            "fixtures" / "woburn-gps.md")
    ap.add_argument("--require-field-crosswalk", action="store_true")
    args = ap.parse_args()
    if not args.openkc_script.is_file():
        ap.error("Original Scratchpad OpenKC script was not found")
    original = load_original(args.openkc_script)
    raw = args.fixture.read_bytes()
    ast = original.ast_from_bytes(raw, args.fixture.name)
    okf = original.ast_to_okf(ast)
    meta, body = original.split_note(okf)
    recovered = original.okf_to_ast(okf)
    bytes_preserved = original.base64.b64decode(recovered["source_base64"]) == raw
    ast_preserved = recovered == ast
    mapped_fields = {field: field in meta for field in FIELDS}
    report = {
        "source": str(args.fixture),
        "implementation": str(args.openkc_script),
        "source_sha256": original.sha(raw),
        "source_bytes_preserved": bytes_preserved,
        "AST_preserved": ast_preserved,
        "okf_metadata_keys": list(meta),
        "original_body_preserved": body.encode("utf-8") == raw,
        "literal_gps_values_in_source": all(
            value in body for value in ("Woburn", "01801", "42.479261", "-71.152278")
        ),
        "individually_mapped_gps_fields": mapped_fields,
        "field_level_crosswalk_complete": all(mapped_fields.values()),
        "classification": "characterization; not UKC SDK conformance",
    }
    print(json.dumps(report, indent=2))
    assert bytes_preserved and ast_preserved and report["original_body_preserved"]
    assert report["literal_gps_values_in_source"]
    if args.require_field_crosswalk and not report["field_level_crosswalk_complete"]:
        raise SystemExit("MISSING: direct OKF field-level GPS crosswalk")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
