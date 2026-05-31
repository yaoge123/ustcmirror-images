#!/usr/bin/env python3
# A simple script to scan index file, and remove nonexisting crate folder.

import os
from pathlib import Path
import sys
import argparse

from utils_crates import iter_index_files

dry_run = os.environ.get("CRATES_DRY_RUN", "false").lower() in {
    "1",
    "true",
    "yes",
    "on",
}


def main(index_dir: Path, crates_dir: Path):
    indexes = set()
    for entry in iter_index_files(index_dir):
        indexes.add(Path(entry).name.lower())

    crate_mapping = {}
    crates = set()
    for entry in os.scandir(crates_dir):
        if entry.is_dir():
            original_name = entry.name
            lower_name = original_name.lower()
            if lower_name != original_name:
                crate_mapping[lower_name] = original_name
            crates.add(entry.name.lower())

    for lower_name in crates - indexes:
        folder_name = crate_mapping.get(lower_name, lower_name)
        if not folder_name:
            continue
        if dry_run:
            print(f"[INFO] {folder_name} shall be removed (dry run)")
        else:
            print(f"[INFO] {folder_name} shall be removed")
            os.removedirs(crates_dir / folder_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Rust crates.io cleanup script")
    parser.add_argument("--index", required=True, type=Path)
    parser.add_argument("--crates", required=True, type=Path)
    args = parser.parse_args()

    try:
        raise SystemExit(main(args.index, args.crates))
    except Exception as exc:
        print(f"[FATAL] {exc}", file=sys.stderr)
        raise
