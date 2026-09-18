#!/usr/bin/env python3
"""
Claude Code Stop hook for qorix-ik: Automatic nexus lifecycle enforcement.

This hook runs at the end of every Claude Code session. It checks the nexus
lifecycle state and automatically stages any complete PI items that have not
yet been promoted to staged, preventing the manual step from being forgotten.

This hook is part of the qik scaffold and is wired into .claude/settings.json
under StopHook (fires after the session completes).
"""

import sys
import os
import subprocess
import json
from pathlib import Path
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Fallback for older Python


def find_project_root(start_dir: str = ".") -> Path:
    """Find the project root by walking up for .qik/nexus/entries.toml."""
    current = Path(start_dir).resolve()
    while current != current.parent:
        nexus_file = current / ".qik" / "nexus" / "entries.toml"
        if nexus_file.exists():
            return current
        current = current.parent
    return None


def get_pi_entries_status(project_root: Path) -> dict:
    """
    Check nexus lifecycle status and identify complete items that need staging.
    
    Returns:
      {
        "complete_items": [(id, headline), ...],
        "already_staged": [(id, headline), ...],
        "incomplete_items": [(id, headline), ...],
      }
    """
    nexus_file = project_root / ".qik" / "nexus" / "entries.toml"
    if not nexus_file.is_file():
        return {"complete_items": [], "already_staged": [], "incomplete_items": []}

    try:
        with open(nexus_file, "rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        print(f"warning: could not read nexus store: {e}", file=sys.stderr)
        return {"complete_items": [], "already_staged": [], "incomplete_items": []}

    complete_items = []
    already_staged = []
    incomplete_items = []

    if "entry" in data:
        for entry in data["entry"]:
            entry_id = entry.get("id", "?")
            headline = entry.get("headline", "(no headline)")
            stage = entry.get("stage", "").lower()
            progress = entry.get("progress", "").lower()

            if stage == "pi" and progress == "complete":
                complete_items.append((entry_id, headline))
            elif stage == "staged":
                already_staged.append((entry_id, headline))
            elif stage == "pi":
                incomplete_items.append((entry_id, headline))

    return {
        "complete_items": complete_items,
        "already_staged": already_staged,
        "incomplete_items": incomplete_items,
    }


def promote_complete_items(project_root: Path, items: list) -> bool:
    """
    Automatically promote complete items to staged using qik nexus promote.
    
    Args:
      project_root: Path to project root
      items: List of (id, headline) tuples to promote
    
    Returns:
      True if all promotions succeeded, False otherwise
    """
    if not items:
        return True

    all_ok = True
    for item_id, headline in items:
        try:
            result = subprocess.run(
                ["qik", "nexus", "promote", item_id],
                cwd=str(project_root),
                capture_output=True,
                timeout=10,
                text=True,
            )
            if result.returncode == 0:
                print(
                    f"  ✓ staged {item_id}: {headline}",
                    file=sys.stderr,
                )
            else:
                print(
                    f"  ✗ failed to stage {item_id}: {result.stderr}",
                    file=sys.stderr,
                )
                all_ok = False
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"  ✗ could not run qik nexus promote: {e}", file=sys.stderr)
            all_ok = False

    return all_ok


def main():
    """Entry point for the Stop hook."""
    # Find project root
    project_root = find_project_root(".")
    if not project_root:
        # Not a qik project, silently continue
        return 0

    # Check nexus status
    status = get_pi_entries_status(project_root)
    complete_items = status["complete_items"]

    if not complete_items:
        # No complete items, nothing to do
        return 0

    # Notify the user and auto-promote
    print(
        f"\n[qik-nexus-lifecycle] Detected {len(complete_items)} complete PI item(s) "
        "that have not yet been staged.",
        file=sys.stderr,
    )

    # Attempt to auto-promote
    print("[qik-nexus-lifecycle] Staging complete items...", file=sys.stderr)
    if promote_complete_items(project_root, complete_items):
        print(
            f"[qik-nexus-lifecycle] ✓ Successfully staged {len(complete_items)} item(s)",
            file=sys.stderr,
        )
        return 0
    else:
        print(
            "[qik-nexus-lifecycle] ✗ Some items could not be auto-staged; "
            "please run 'qik nexus promote' manually.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
