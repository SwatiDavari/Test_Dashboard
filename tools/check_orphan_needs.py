#!/usr/bin/env python3
"""Traceability gate: fail CI if any sphinx-needs 'need' has no incoming
or outgoing links. Run after `sphinx-build -b needs`."""
import json
import sys

def main(path: str) -> int:
    with open(path) as f:
        data = json.load(f)
    orphans = []
    for version in data.get("versions", {}).values():
        for need_id, need in version.get("needs", {}).items():
            if not need.get("links") and not need.get("links_back"):
                orphans.append(need_id)
    if orphans:
        print("Orphan needs found (no traceability links):")
        for o in orphans:
            print(f"  - {o}")
        return 1
    print("No orphan needs found.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "_build/needs/needs.json"))
