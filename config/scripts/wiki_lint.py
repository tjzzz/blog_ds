#!/usr/bin/env python3
"""Validate the local DS Wiki migration and public site inputs."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote
import yaml

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT
PUBLIC_FILES = [DOCS / name for name in ('index.md', 'about.md', 'wiki-log.md', 'wiki-schema.md')]
PUBLIC_DIRS = [DOCS / name for name in ('topics', 'relationships', 'syntheses', 'media', 'js')]
SOURCE = ROOT / 'Input/rebuild_source_2026-10-09'
LEGACY_SOURCE = ROOT / 'Input/legacy_docs_2026-10-09'
MIGRATION = json.loads((ROOT / 'config/scripts/wiki_migration_map.json').read_text())
MANIFEST_PATH = SOURCE / '_manifest.json'
LEGACY_MANIFEST_PATH = LEGACY_SOURCE / '_manifest.json'
ERRORS: list[str] = []
FIELDS = {'title','created','updated','tags','source','topic','wiki_type','migrated_from','review_status'}
PRIVATE_TOPICS = {'深度学习', '业务指标与诊断', '轨迹分析', '编程与数据工程'}
PUBLIC_TOPICS = ('数据科学工作流','统计学基础','实验设计与AB测试','因果推断','机器学习',
                 '推荐系统','数字零售与商业空间','算法与面试','AI与Agent')
LINK = re.compile(r'!?\[[^\]\n]*\]\(([^)\n]+)\)')
SECRET = re.compile(r'sk-[A-Za-z0-9_-]{20,}')
IMAGE_EXT = {'.png','.jpg','.jpeg','.gif','.webp','.svg','.bmp','.tif','.tiff'}

source_count = MIGRATION['source_count']
snapshot_state = 'private snapshot unavailable'
if MANIFEST_PATH.is_file():
    manifest = json.loads(MANIFEST_PATH.read_text())
    if len(manifest['files']) != source_count:
        ERRORS.append('source snapshot count differs from public migration map')
    for rel, expected in manifest['files'].items():
        path = SOURCE / rel
        if not path.is_file():
            ERRORS.append(f'missing source: {rel}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            ERRORS.append(f'changed source snapshot: {rel}')
    snapshot_state = 'full private snapshot verified'
elif LEGACY_MANIFEST_PATH.is_file():
    legacy_manifest = json.loads(LEGACY_MANIFEST_PATH.read_text())
    for rel, expected in legacy_manifest['files'].items():
        path = LEGACY_SOURCE / rel
        if not path.is_file():
            ERRORS.append(f'missing legacy backup: {rel}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            ERRORS.append(f'changed legacy backup: {rel}')
    snapshot_state = f"full snapshot missing; {len(legacy_manifest['files'])} legacy files verified"

for old, new in MIGRATION['mapping'].items():
    private = new.startswith('topics/') and new.split('/')[1] in PRIVATE_TOPICS
    page = DOCS/'Input'/Path(new).relative_to('topics') if private else DOCS/new
    alias = DOCS/old
    if not page.is_file():
        ERRORS.append(f'missing migrated page: {page.relative_to(DOCS)}')
        continue
    if alias.exists(): ERRORS.append(f'legacy page still in docs: {old}')
    if private:
        continue
    text = page.read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---\n',text,re.S)
    if not match:
        ERRORS.append(f'missing frontmatter: {new}')
        continue
    try: meta=yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        ERRORS.append(f'invalid frontmatter: {new}: {exc}')
        continue
    required = FIELDS - {'migrated_from'} if new.startswith('topics/') and new.endswith('/index.md') else FIELDS
    for field in required-set(meta): ERRORS.append(f'{new}: missing {field}')
    if new.startswith('topics/') and new.endswith('/index.md'):
        if old not in meta.get('merged_from', []):
            ERRORS.append(f'{new}: missing merged source {old}')
        if f'Input/rebuild_source_2026-10-09/{old}' not in meta.get('source', []):
            ERRORS.append(f'{new}: missing source citation {old}')
    elif meta.get('migrated_from') != old:
        ERRORS.append(f'{new}: wrong migrated_from')
    expected_types = {'topic'} if new.startswith('topics/') and new.endswith('/index.md') else {'topics','concepts','methods','tools','cases'}
    if meta.get('wiki_type') not in expected_types:
        ERRORS.append(f'{new}: invalid wiki_type')
    if meta.get('review_status') != 'structural': ERRORS.append(f'{new}: unexpected review_status')

public_pages = PUBLIC_FILES + [page for folder in PUBLIC_DIRS for page in folder.rglob('*.md')]
for page in public_pages:
    if len(page.relative_to(DOCS).parts) > 4:
        ERRORS.append(f'page exceeds Topic / subtopic depth: {page.relative_to(DOCS)}')
    text=page.read_text(encoding='utf-8')
    frontmatter = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if not frontmatter or not re.search(r'(?m)^wiki_type:', frontmatter.group(1)):
        ERRORS.append(f'missing wiki_type: {page.relative_to(DOCS)}')
    if SECRET.search(text): ERRORS.append(f'possible private credential: {page.relative_to(ROOT)}')
    if '/Users/' in text or re.search(r'\b[A-Za-z0-9._%+-]+@163\.com\b',text,re.I):
        ERRORS.append(f'possible private identifier: {page.relative_to(ROOT)}')
    for raw in LINK.findall(text):
        target=unquote(raw.split('#',1)[0]).strip('<>')
        if not target or target.startswith(('http://','https://','mailto:','data:')): continue
        if Path(target).suffix.lower() in IMAGE_EXT:
            resolved=(page.parent/target).resolve()
            if not any(resolved.is_relative_to(folder.resolve()) for folder in PUBLIC_DIRS) or not resolved.is_file():
                ERRORS.append(f'broken/private image: {page.relative_to(ROOT)} -> {raw}')

for topic in PUBLIC_TOPICS:
    page=DOCS/'topics'/topic/'index.md'
    if not page.is_file(): ERRORS.append(f'missing Topic: {topic}')
    if (DOCS/'topics'/f'{topic}.md').exists():
        ERRORS.append(f'duplicate Topic entry: {topic}')
    for subtopic in (DOCS/'topics'/topic).iterdir():
        if subtopic.is_dir() and not (subtopic/'index.md').is_file():
            ERRORS.append(f'missing subtopic index: {subtopic.relative_to(DOCS)}')

for path in (path for folder in PUBLIC_DIRS for path in folder.rglob('*')):
    if path.is_file() and len(path.relative_to(DOCS).parts) > 4:
        ERRORS.append(f'asset exceeds Topic / subtopic depth: {path.relative_to(DOCS)}')

missing_images = len(list((DOCS/'media/missing').glob('*.svg')))
print(f"Source snapshots: {source_count} ({snapshot_state}); migrated articles: {len(MIGRATION['mapping'])}; "
      f"public Topic pages: {len(PUBLIC_TOPICS)}; unrecovered originals: {missing_images}; errors: {len(ERRORS)}")
for item in ERRORS[:30]: print(item)
raise SystemExit(bool(ERRORS))
