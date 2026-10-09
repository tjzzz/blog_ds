#!/usr/bin/env python3
"""Validate the local DS Wiki migration and public site inputs."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote
import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SOURCE = ROOT / 'Input/rebuild_source_2026-10-09'
MIGRATION = json.loads((ROOT / 'scripts/wiki_migration_map.json').read_text())
MANIFEST_PATH = SOURCE / '_manifest.json'
ERRORS: list[str] = []
FIELDS = {'title','created','updated','tags','source','topic','wiki_type','migrated_from','review_status'}
LINK = re.compile(r'!?\[[^\]\n]*\]\(([^)\n]+)\)')
SECRET = re.compile(r'sk-[A-Za-z0-9_-]{20,}')
IMAGE_EXT = {'.png','.jpg','.jpeg','.gif','.webp','.svg','.bmp','.tif','.tiff'}

source_count = MIGRATION['source_count']
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

for old, new in MIGRATION['mapping'].items():
    page, alias = DOCS/new, DOCS/old
    if not page.is_file():
        ERRORS.append(f'missing migrated page: {new}')
        continue
    if alias.exists(): ERRORS.append(f'legacy page still in docs: {old}')
    text = page.read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---\n',text,re.S)
    if not match:
        ERRORS.append(f'missing frontmatter: {new}')
        continue
    try: meta=yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        ERRORS.append(f'invalid frontmatter: {new}: {exc}')
        continue
    for field in FIELDS-set(meta): ERRORS.append(f'{new}: missing {field}')
    if meta.get('migrated_from') != old: ERRORS.append(f'{new}: wrong migrated_from')
    if meta.get('wiki_type') not in {'topics','concepts','methods','tools','cases'}:
        ERRORS.append(f'{new}: invalid wiki_type')
    if meta.get('review_status') != 'structural': ERRORS.append(f'{new}: unexpected review_status')

for page in DOCS.rglob('*.md'):
    if len(page.relative_to(DOCS).parts) > 3:
        ERRORS.append(f'page exceeds two folder levels: {page.relative_to(DOCS)}')
    text=page.read_text(encoding='utf-8')
    if SECRET.search(text): ERRORS.append(f'possible private credential: {page.relative_to(ROOT)}')
    if '/Users/' in text or re.search(r'\b[A-Za-z0-9._%+-]+@163\.com\b',text,re.I):
        ERRORS.append(f'possible private identifier: {page.relative_to(ROOT)}')
    for raw in LINK.findall(text):
        target=unquote(raw.split('#',1)[0]).strip('<>')
        if not target or target.startswith(('http://','https://','mailto:','data:')): continue
        if Path(target).suffix.lower() in IMAGE_EXT:
            resolved=(page.parent/target).resolve()
            if not resolved.is_relative_to(DOCS.resolve()) or not resolved.is_file():
                ERRORS.append(f'broken/private image: {page.relative_to(ROOT)} -> {raw}')

for topic in ('数据科学工作流','统计学基础','实验设计与AB测试','因果推断','机器学习','深度学习',
              '推荐系统','编程与数据工程','业务指标与诊断','数字零售与商业空间','轨迹分析','算法与面试','AI与Agent'):
    page=DOCS/'topics'/f'{topic}.md'
    if not page.is_file(): ERRORS.append(f'missing Topic: {topic}')

for path in DOCS.rglob('*'):
    if path.is_file() and len(path.relative_to(DOCS).parts) > 3:
        ERRORS.append(f'asset exceeds two folder levels: {path.relative_to(DOCS)}')

snapshot_state = 'verified' if MANIFEST_PATH.is_file() else 'private snapshot unavailable'
missing_images = len(list((DOCS/'media/missing').glob('*.svg')))
print(f"Source snapshots: {source_count} ({snapshot_state}); migrated articles: {len(MIGRATION['mapping'])}; "
      f"Topic pages: 13; unrecovered originals: {missing_images}; errors: {len(ERRORS)}")
for item in ERRORS[:30]: print(item)
raise SystemExit(bool(ERRORS))
