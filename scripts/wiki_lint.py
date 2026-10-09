#!/usr/bin/env python3
"""Check the public LLM Wiki layer before publishing."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SECTIONS = ('topics', 'entities', 'relationships', 'syntheses')
FIELDS = {'title', 'created', 'updated', 'tags', 'source', 'status'}
LINK = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
errors = []
count = 0
for section in SECTIONS:
    for page in sorted((DOCS / section).glob('*.md')):
        count += 1
        content = page.read_text(encoding='utf-8')
        match = re.match(r'\A---\n(.*?)\n---\n', content, re.S)
        if not match:
            errors.append(f'{page.relative_to(ROOT)}: missing YAML frontmatter')
            continue
        meta = yaml.safe_load(match.group(1)) or {}
        for field in sorted(FIELDS - set(meta)):
            errors.append(f'{page.relative_to(ROOT)}: missing {field}')
        if meta.get('status') not in {'inventory', 'pilot', 'reviewed'}:
            errors.append(f'{page.relative_to(ROOT)}: invalid status')
        if not isinstance(meta.get('source'), list):
            errors.append(f'{page.relative_to(ROOT)}: source must be a list')
        for source in meta.get('source', []):
            if not isinstance(source, str):
                errors.append(f'{page.relative_to(ROOT)}: non-string source')
            elif not source.startswith(('http://', 'https://')) and not (ROOT / source).is_file():
                errors.append(f'{page.relative_to(ROOT)}: missing source {source}')
        for raw in LINK.findall(content):
            target = unquote(raw.split('#', 1)[0])
            if not target or target.startswith(('http://', 'https://', 'mailto:')):
                continue
            if not (page.parent / target).resolve().is_file():
                errors.append(f'{page.relative_to(ROOT)}: broken link {raw}')
print(f'Checked {count} Wiki pages; {len(errors)} errors')
for error in errors:
    print(error, file=sys.stderr)
sys.exit(bool(errors))
