"""Shared path filters for scanner inputs."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterator, Optional, Set

# Default directories to skip during file collection.
DEFAULT_SKIP_DIRS: Set[str] = {
    ".git",
    ".github",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    "coverage",
    ".mypy_cache",
    ".pytest_cache",
    ".tox",
    ".eggs",
    "*.egg-info",
}

# Default file extensions to include (source files only).
DEFAULT_EXTENSIONS: Set[str] = {
    ".py",
    ".ts",
    ".js",
    ".tsx",
    ".jsx",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".sh",
    ".bash",
    ".zsh",
    ".cfg",
    ".ini",
    ".txt",
    ".plist",
    ".service",
}

_WALK_CACHE: dict[tuple[str, tuple[str, ...]], list[Path]] = {}


def iter_source_files(
    target: Path,
    *,
    skip_dirs: Optional[Set[str]] = None,
    extensions: Optional[Set[str]] = None,
    max_files: int = 0,
) -> Iterator[Path]:
    """Efficiently walk a directory tree, yielding only relevant source files.

    Instead of ``target.rglob("*")`` which traverses every file and directory,
    this function prunes skip-dirs early (during os.walk) and only yields files
    with matching extensions. This is typically 5–10x faster on large projects.

    Args:
        target: Root directory to scan (or a single file path).
        skip_dirs: Directory names to prune. Defaults to DEFAULT_SKIP_DIRS.
        extensions: File extensions to include. Defaults to DEFAULT_EXTENSIONS.
            Empty set means include all files.
        max_files: Stop after yielding this many files (0 = unlimited).

    Yields:
        Path objects for each matching file.
    """
    if target.is_file():
        yield target
        return

    skip = DEFAULT_SKIP_DIRS if skip_dirs is None else skip_dirs
    exts = extensions if extensions is not None else DEFAULT_EXTENSIONS
    skip_lower = frozenset(item.lower() for item in skip)
    cache_key = (str(target.resolve()), tuple(sorted(skip_lower)))

    files = _WALK_CACHE.get(cache_key)
    if files is None:
        files = []
        for dirpath, dirnames, filenames in os.walk(target):
            # Prune skipped directories in-place to prevent descent.
            dirnames[:] = [d for d in dirnames if d.lower() not in skip_lower and not d.endswith(".egg-info")]

            for fname in filenames:
                fp = Path(dirpath) / fname
                if looks_generated_asset(fp):
                    continue
                files.append(fp)
        _WALK_CACHE[cache_key] = files

    count = 0
    for fp in files:
        if exts and fp.suffix not in exts:
            continue
        yield fp
        count += 1
        if max_files and count >= max_files:
            return


GENERATED_ASSET_DIR_HINTS = {
    "assets",
    "_assets",
    "static",
    "generated",
    "vendor",
}

HASHED_BUNDLE_RE = re.compile(
    r"^(?:chunk|blockdiagram|vendor|runtime|mermaid|graph|worker|index|app|main)"
    r"-[a-z0-9_-]{6,}(?:-[a-z0-9_-]{4,})*(?: \d+)?\.(?:js|cjs|mjs)$",
    re.IGNORECASE,
)
GENERIC_HASHED_ASSET_RE = re.compile(
    r"^[a-z0-9_.-]+-[a-z0-9_-]{8,}(?: \d+)?\.(?:js|cjs|mjs|css|map)$",
    re.IGNORECASE,
)
MINIFIED_JS_RE = re.compile(r".*\.min\.(?:js|cjs|mjs)$", re.IGNORECASE)


def should_skip_path(path: Path, skip_dirs: set[str]) -> bool:
    """Return True when a path should be ignored by behavior-focused scanners."""

    lowered_parts = {part.lower() for part in path.parts}
    if any(skip_dir.lower() in lowered_parts for skip_dir in skip_dirs):
        return True
    return looks_generated_asset(path)


def looks_generated_asset(path: Path) -> bool:
    """Detect generated or minified front-end asset bundles."""

    lowered_parts = {part.lower() for part in path.parts}
    name = path.name

    if MINIFIED_JS_RE.match(name):
        return True

    if not any(part in GENERATED_ASSET_DIR_HINTS for part in lowered_parts):
        return False

    return bool(HASHED_BUNDLE_RE.match(name) or GENERIC_HASHED_ASSET_RE.match(name))
