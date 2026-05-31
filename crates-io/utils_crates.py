import os
from pathlib import Path


def is_tracked_index_file(rel: Path) -> bool:
    return len(rel.parts) >= 2 and all(
        not part.startswith(".") for part in rel.parts[:-1]
    )


def iter_index_files(index_dir: Path):
    stack = [str(index_dir)]
    while stack:
        # Performance: pathlib is not used here as it calls stat for every file, too slow.
        for entry in os.scandir(stack.pop()):
            if entry.is_dir(follow_symlinks=False):
                stack.append(entry.path)
            elif entry.is_file():
                rel = Path(entry.path).relative_to(index_dir)
                if is_tracked_index_file(rel):
                    yield Path(entry.path)
