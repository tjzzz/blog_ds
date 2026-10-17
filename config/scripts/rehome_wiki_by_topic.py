#!/usr/bin/env python3
"""One-time migration from type/topic pages to topic pages.

Run from the repository root. The script is deliberately strict about filename
collisions and rewrites local Markdown links from their original locations.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
TYPES = ("concepts", "methods", "tools", "cases")
TYPE_NAMES = {"concepts": "概念", "methods": "方法", "tools": "工具", "cases": "案例"}
MAP_PATH = ROOT / "config/scripts/wiki_migration_map.json"
NOT_FOUND = ROOT / "config/overrides/404.html"


def markdown_links(text: str, old_page: Path, new_page: Path, moves: dict[Path, Path]) -> str:
    """Move relative link targets with their source page, including images."""
    # A Scala type call such as ``ofDim[Int](3, 3)`` also contains "]("
    # but must not be interpreted as a Markdown link.
    fences = []
    opening = None
    for match in re.finditer(r"(?m)^\s*(`{3,}|~{3,})[^\n]*$", text):
        if opening is None:
            opening = (match.start(), match.group(1)[0], len(match.group(1)))
        elif match.group(1)[0] == opening[1] and len(match.group(1)) >= opening[2]:
            fences.append((opening[0], match.end()))
            opening = None
    if opening is not None:
        fences.append((opening[0], len(text)))
    chunks: list[str] = []
    cursor = 0
    while True:
        start = text.find("](", cursor)
        if start < 0:
            chunks.append(text[cursor:])
            break
        if any(lo <= start < hi for lo, hi in fences):
            chunks.append(text[cursor:start + 2])
            cursor = start + 2
            continue
        chunks.append(text[cursor:start + 2])
        pos, nesting = start + 2, 1
        while pos < len(text) and nesting:
            if text[pos] == "(" and (pos == 0 or text[pos - 1] != "\\"):
                nesting += 1
            elif text[pos] == ")" and (pos == 0 or text[pos - 1] != "\\"):
                nesting -= 1
            pos += 1
        if nesting:
            chunks.append(text[start + 2:])
            break
        raw = text[start + 2:pos - 1]
        target = raw
        if raw and not raw.startswith(("#", "//", "<", "data:")):
            parts = urlsplit(raw)
            if not parts.scheme and parts.path and not parts.path.startswith("/"):
                old_target = (old_page.parent / unquote(parts.path)).resolve()
                if old_target.is_relative_to(DOCS.resolve()):
                    new_target = moves.get(old_target, old_target)
                    rel = os.path.relpath(new_target, new_page.parent)
                    target = "/".join(quote(piece, safe="-._~") for piece in Path(rel).parts)
                    if parts.query:
                        target += "?" + parts.query
                    if parts.fragment:
                        target += "#" + parts.fragment
        chunks.append(target + ")")
        cursor = pos
    return "".join(chunks)


def ensure_type(text: str, kind: str) -> str:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("Missing YAML front matter")
    if re.search(r"(?m)^wiki_type:", match.group(1)):
        return text
    return text[:match.end(1)] + f"\nwiki_type: {kind}" + text[match.end(1):]


def main() -> None:
    old_files = [p for kind in TYPES for p in (DOCS / kind).glob("*/*.md")]
    moves = {
        old.resolve(): (DOCS / "topics" / old.parent.name / old.name).resolve()
        for old in old_files
    }
    if len(set(moves.values())) != len(moves) or any(new.exists() for new in moves.values()):
        raise SystemExit("Target filename collision; inspect before migrating")

    old_to_kind = {p.resolve(): p.parent.parent.name for p in old_files}
    # Read everything before changing any path so relative links resolve from
    # the original page locations.
    pages = {p.resolve(): p.read_text(encoding="utf-8") for p in DOCS.rglob("*.md")}
    for old, content in pages.items():
        if old in {(DOCS / kind / "index.md").resolve() for kind in TYPES}:
            continue
        new = moves.get(old, old)
        updated = markdown_links(content, old, new, moves)
        if old in old_to_kind:
            updated = ensure_type(updated, old_to_kind[old])
        elif old.parent == (DOCS / "relationships").resolve():
            updated = ensure_type(updated, "relationship")
        elif old.parent == (DOCS / "syntheses").resolve():
            updated = ensure_type(updated, "synthesis")
        elif old in {(DOCS / name).resolve() for name in ("index.md", "about.md", "wiki-schema.md", "wiki-log.md")}:
            if content.startswith("---\n"):
                updated = ensure_type(updated, "site")
        new.parent.mkdir(parents=True, exist_ok=True)
        new.write_text(updated, encoding="utf-8")

    for old in moves:
        old.unlink()
    for kind in TYPES:
        (DOCS / kind / "index.md").unlink()
        for child in (DOCS / kind).iterdir():
            if child.is_dir():
                child.rmdir()
        (DOCS / kind).rmdir()

    migration = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    previous = dict(migration["mapping"])
    migration["mapping"] = {
        old: moves.get((DOCS / new).resolve(), (DOCS / new).resolve()).relative_to(DOCS.resolve()).as_posix()
        for old, new in previous.items()
    }
    MAP_PATH.write_text(json.dumps(migration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Preserve both the original legacy addresses and the recently published
    # type/topic addresses.
    redirect = {
        old.removesuffix(".md"): new.removesuffix("/index.md").removesuffix(".md")
        for old, new in migration["mapping"].items()
    }
    for old, new in moves.items():
        redirect[old.relative_to(DOCS).with_suffix("").as_posix()] = new.relative_to(DOCS).with_suffix("").as_posix()
    html = NOT_FOUND.read_text(encoding="utf-8")
    payload = json.dumps(redirect, ensure_ascii=False, separators=(",", ":"))
    html = re.sub(r"(?m)^const oldToNew=.*;$", "const oldToNew=" + payload + ";", html)
    NOT_FOUND.write_text(html, encoding="utf-8")
    print(f"Moved {len(moves)} pages into {len({p.parent for p in moves.values()})} topics")


if __name__ == "__main__":
    main()
