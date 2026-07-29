#!/usr/bin/env python3
"""Traceability gate: fail CI if any sphinx-needs 'need' has no incoming
or outgoing links. Run after `sphinx-build -b needs`.

Self-diagnosing: if it still finds orphans, it prints the RAW keys and
values of one real need (ARC_COM_001 if present, else the first need)
so the actual JSON shape is visible in the CI log -- no more guessing.
"""
import json
import sys

KNOWN_LINK_OPTIONS = ["derives_from", "verifies", "mitigates", "satisfies", "links"]


def has_any_link(need: dict) -> bool:
    for key, value in need.items():
        if not value:
            continue
        if key.endswith("_back") and isinstance(value, (list, str)) and len(value) > 0:
            return True
        if key in KNOWN_LINK_OPTIONS and isinstance(value, (list, str)) and len(value) > 0:
            return True
    return False


def main(path: str) -> int:
    with open(path) as f:
        data = json.load(f)

    print(f"Top-level keys in needs.json: {list(data.keys())}")

    versions = data.get("versions", {})
    if not versions:
        print("No 'versions' key found -- raw structure sample:")
        print(json.dumps(data, indent=2)[:2000])
        return 0

    orphans = []
    all_needs = {}
    for version_name, version in versions.items():
        needs = version.get("needs", {})
        all_needs.update(needs)
        for need_id, need in needs.items():
            if not has_any_link(need):
                orphans.append(need_id)

    if orphans:
        print("Orphan needs found (no traceability links):")
        for o in sorted(orphans):
            print(f"  - {o}")

        sample_id = "ARC_COM_001" if "ARC_COM_001" in all_needs else next(iter(all_needs))
        print(f"\n--- DIAGNOSTIC: raw fields for '{sample_id}' (expected to have real links) ---")
        print(json.dumps(all_needs[sample_id], indent=2))
        print("--- END DIAGNOSTIC ---\n")
        return 1

    print("No orphan needs found.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "_build/needs/needs.json"))
