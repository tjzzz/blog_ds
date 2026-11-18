"""Mount the external 资讯 folder as a top-level tab of the blog.

The folder lives next to the repo in the Obsidian vault, outside ``docs_dir``.
Rather than copying files into the repo (which would create a duplicate source
of truth) or committing a symlink (which dangles on CI), this hook injects the
Markdown files into the MkDocs file collection at build time via
``File.generated()``. The source folder is only read, never written to.

If the folder is absent -- e.g. on CI, where only the repository is checked out
-- the hook is a no-op: no tab, no injected pages, and the build stays green.
The public site is therefore published from a local build that has the folder,
not from CI (see .github/workflows/ci.yml).

Env:
    BLOG_NEWS_DIR  Override the external folder path. Defaults to
                   ``<docs_dir>/../资讯`` -- a relative path, so no
                   machine-specific absolute path is committed.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from mkdocs.structure.files import File, InclusionLevel

FOLDER_NAME = "资讯"
URI_PREFIX = "资讯"
TAB_LABEL = "资讯"
INDEX_LABEL = "总览"
HEADING = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
GLUED_URL = re.compile(r"(https?://[!-~]+)(?=[^\x00-\x7f])")


def _sanitize(text):
    """Keep bare URLs from swallowing adjacent full-width punctuation.

    The briefs use '｜' and '：' as separators, e.g.
    ``https://a.com｜中文：https://b.com``. pymdownx.magiclink then treats the
    whole run as one URL whose netloc contains full-width characters, which
    Python 3.12+ rejects under NFKC validation and aborts the build. Inserting
    a space at the boundary fixes the published copy only; the source notes
    in the vault are never modified.
    """
    text = text.replace("｜", " ｜ ")
    return GLUED_URL.sub(r"\1 ", text)


def _root(config):
    override = os.environ.get("BLOG_NEWS_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return (Path(config["docs_dir"]).parent / FOLDER_NAME).resolve()


def _title(path):
    text = path.read_text(encoding="utf-8")
    match = HEADING.search(text[:4000])
    return match.group(1).strip() if match else path.stem


def _pages(root):
    """Return (src_uri, abs_path, label, group, rel) for publishable .md files.

    Dot-prefixed dirs/files are skipped: they hold editor metadata and agent
    memory (``.workbuddy/memory``), which must never reach a public site.
    """
    pages = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        rel_dir = Path(dirpath).relative_to(root)
        for name in sorted(f for f in filenames if f.endswith(".md") and not f.startswith(".")):
            path = Path(dirpath) / name
            rel = (rel_dir / name).as_posix() if str(rel_dir) != "." else name
            parts = rel.split("/")
            group = parts[0] if len(parts) > 1 else ""
            pages.append((f"{URI_PREFIX}/{rel}", path, Path(name).stem, group, rel))
    return pages


def _nav(pages):
    groups = {}
    for uri, _path, label, group, _rel in pages:
        groups.setdefault(group, []).append({label: uri})

    def by_label(items):
        return sorted(items, key=lambda item: next(iter(item)), reverse=True)

    nav = [{INDEX_LABEL: f"{URI_PREFIX}/index.md"}]
    for group in sorted(g for g in groups if g):
        nav.append({group: by_label(groups[group])})
    if "" in groups:
        nav.extend(by_label(groups[""]))
    return nav


def _index(pages):
    groups = {}
    for _uri, path, _label, group, rel in pages:
        groups.setdefault(group, []).append((rel, _title(path)))
    lines = [f"# {TAB_LABEL}", ""]
    for group in sorted(g for g in groups if g):
        lines += [f"## {group}", ""]
        for rel, title in sorted(groups[group], reverse=True):
            lines.append(f"- [{title}]({rel})")
        lines.append("")
    if "" in groups:
        for rel, title in sorted(groups[""], reverse=True):
            lines.append(f"- [{title}]({rel})")
    return "\n".join(lines) + "\n"


def on_config(config):
    root = _root(config)
    if not root.is_dir():
        return config
    pages = _pages(root)
    if not pages:
        return config

    nav = config["nav"] or []
    if not any(isinstance(entry, dict) and TAB_LABEL in entry for entry in nav):
        nav.append({TAB_LABEL: _nav(pages)})
    config["nav"] = nav

    # Let `mkdocs serve` rebuild when a brief in the external folder changes.
    if str(root) not in config["watch"]:
        config["watch"].append(str(root))
    return config


def on_files(files, config):
    root = _root(config)
    if not root.is_dir():
        return files
    pages = _pages(root)
    if not pages:
        return files

    for uri, path, _label, _group, _rel in pages:
        files.append(
            File.generated(
                config,
                uri,
                content=_sanitize(path.read_text(encoding="utf-8")),
                inclusion=InclusionLevel.INCLUDED,
            )
        )
    files.append(
        File.generated(
            config,
            f"{URI_PREFIX}/index.md",
            content=_index(pages),
            inclusion=InclusionLevel.INCLUDED,
        )
    )
    return files
