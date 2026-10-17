"""Build the MkDocs sidebar from the published wiki directories."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
TITLE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
HEADING = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def _title(path):
    content = path.read_text(encoding="utf-8")
    if content.startswith("---\n"):
        frontmatter = content.split("---", 2)[1]
        match = TITLE.search(frontmatter)
        if match:
            return match.group(1).strip('"\'')
    match = HEADING.search(content)
    return match.group(1) if match else path.stem


def _reading_order(directory):
    index = directory / "index.md"
    if not index.exists():
        return {}
    order = {}
    for match in LINK.finditer(index.read_text(encoding="utf-8")):
        target = unquote(urlsplit(match.group(1)).path)
        if not target.endswith(".md"):
            continue
        resolved = (directory / target).resolve()
        if resolved.is_relative_to(directory.resolve()):
            order.setdefault(resolved, len(order))
    return order


def _children(directory, docs_dir):
    order = _reading_order(directory)
    sections = [path for path in directory.iterdir() if path.is_dir() and (path / "index.md").exists()]
    pages = [path for path in directory.glob("*.md") if path.name != "index.md"]

    def sort_key(path):
        target = path / "index.md" if path.is_dir() else path
        return (order.get(target.resolve(), len(order)), path.name.casefold())

    result = []
    for path in sorted(sections + pages, key=sort_key):
        if path.is_dir():
            result.append({path.name: [_index(path, docs_dir), *_children(path, docs_dir)]})
        else:
            result.append({_title(path): path.relative_to(docs_dir).as_posix()})
    return result


def _index(directory, docs_dir):
    return {_title(directory / "index.md"): (directory / "index.md").relative_to(docs_dir).as_posix()}


def on_config(config):
    docs_dir = Path(config["docs_dir"])
    nav = config["nav"]
    for entry in nav:
        if "Topic" in entry:
            topic_nav = entry["Topic"]
            for item in topic_nav:
                label, source = next(iter(item.items()))
                if source == "topics/index.md":
                    continue
                directory = docs_dir / Path(source).parent
                item[label] = [_index(directory, docs_dir), *_children(directory, docs_dir)]
        for label in ("关系", "综合分析"):
            if label in entry:
                directory = docs_dir / Path(entry[label]).parent
                entry[label] = [_index(directory, docs_dir), *_children(directory, docs_dir)]
    config["nav"] = nav
    return config
