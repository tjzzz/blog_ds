#!/usr/bin/env python3
"""One-time migration of Topic articles into subject-specific subdirectories."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

import yaml

from rehome_wiki_by_topic import DOCS, MAP_PATH, NOT_FOUND, markdown_links


TOPICS = DOCS / "topics"


def classify(topic: str, name: str, kind: str) -> str:
    s = name.removesuffix(".md")
    if topic == "AI与Agent":
        if s.startswith("2026") or s.startswith("Discord"):
            return "实践与部署"
        if s.startswith("AIGC-1.0__"):
            if kind == "tools":
                return "模型与工具"
            if "课程" in s or "references" in s:
                return "学习资料"
            return "生成式AI"
        if s in {"agent teams", "openhuman", "skills", "多Agent体系设计方案", "多agent协作模式", "deepseek harnes"}:
            return "Agent架构"
        return "模型与工具"
    if topic == "业务指标与诊断":
        if s.startswith("案例-"):
            return "诊断案例"
        if s in {"指标体系", "指标监测", "指标异动分析", "数据仓库"}:
            return "指标体系与诊断"
        return "业务专题"
    if topic == "因果推断":
        if "__工具__" in s:
            return "软件实现"
        if "__09_资料" in s:
            return "学习资料"
        if "__方法_" in s or "__03_" in s:
            return "准实验方法"
        return "基础与识别"
    if topic == "实验设计与AB测试":
        if s.startswith("Experiment难题__") or s in {"ab实验__07_网络效应与干扰", "ab实验__08_实验治理与护栏"}:
            if "灵敏度" in s:
                return "灵敏度与提效"
            return "复杂场景与治理"
        if s in {"05_提效与高阶实验问题", "CUPED", "ab实验__04_CUPED与方差缩减", "ExperimentDesign__指标变换与实验敏感性"}:
            return "灵敏度与提效"
        if s in {"02_流量域设计与分流", "业务_如何搭建ab平台"} or "__03_抽样平台" in s or "__流量分组" in s:
            return "分流与平台"
        if s in {"03_指标体系与显著性", "ExperimentDesign__04_实验指标设计"}:
            return "指标与统计"
        if s in {"04_判断方法与上线决策"} or s.startswith("ab实验__"):
            return "统计判断与决策"
        return "实验流程与设计"
    if topic == "推荐系统":
        if s.startswith(("实践-", "【实践】", "工程篇")):
            return "工程与实践"
        if s.startswith(("【推荐系统】", "原理篇—1", "原理篇—2")):
            return "基础与协同过滤"
        if s in {"DSSM", "look alike", "Faiss", "序列推荐", "原理篇—冷启动相关", "原理篇-注意力机制"}:
            return "召回与序列推荐"
        return "排序与深度模型"
    if topic == "数字零售与商业空间":
        if "__招商__" in s:
            return "招商与租户"
        if any(x in s for x in ("用户", "消费者", "画像", "mall satisfaction")):
            return "用户分析"
        if any(x in s for x in ("购物中心", "mall运营", "商业地产", "零售空间布局", "动线", "万达")):
            return "商业空间运营"
        return "零售基础与研究"
    if topic == "数据科学工作流":
        if s.startswith("DataVisulization__"):
            return "数据可视化"
        if s.startswith("get_Data__") or s == "数据质量":
            return "数据获取与质量"
        if s.startswith("增强分析__"):
            return "增强分析"
        return "环境与工具"
    if topic == "机器学习":
        if s.startswith("Features&Data__"):
            return "数据与特征"
        if s.startswith(("Classification__", "Regression__")):
            return "分类与回归"
        if s.startswith(("Cluster__", "Abnormal_detect__")):
            return "聚类与异常检测"
        if s.startswith("时间序列__"):
            return "时间序列"
        if s.startswith("1_Auto_tools__") or s == "模型管理与服务":
            return "平台与工程"
        return "基础与模型评估"
    if topic == "深度学习":
        if s.startswith(("NLP__", "rnn__")):
            return "自然语言处理"
        if s.startswith("基础概念__") or s in {"图网络", "强化学习", "训练常见问题"}:
            return "基础与训练"
        return "计算机视觉"
    if topic == "算法与面试":
        if s.startswith(("学习-", "算法-")):
            return "数据结构与算法"
        if s.startswith(("刷题", "@leetcode", "zzz解题", "DS")):
            return "刷题记录"
        return "面试准备"
    if topic == "统计学基础":
        if s.startswith("抽样技术__") or s.startswith("参数估计-"):
            return "抽样与估计"
        if s in {"案例", "生物统计-生存分析"}:
            return "应用案例"
        return "统计基础与推断"
    if topic == "编程与数据工程":
        if s.startswith("python__"):
            return "Python"
        if s.startswith("SQL__"):
            return "SQL"
        if s.startswith("R__") or s == "scala":
            return "R与Scala"
        if s.startswith("hadoop&spark__"):
            return "Spark与Hadoop"
        return "TensorFlow"
    if topic == "轨迹分析":
        if s.endswith(("__工具", "__轨迹分析-应用案例")):
            return "工具与应用"
        if any(x in s for x in ("-1.trajectory", "-2 轨迹", "-CATS")):
            return "轨迹处理方法"
        return "基础与综述"
    raise ValueError(f"Unrecognized topic: {topic}")


def title_of(text: str, filename: str) -> str:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if match:
        meta = yaml.safe_load(match.group(1)) or {}
        return str(meta.get("title") or filename.removesuffix(".md"))
    return filename.removesuffix(".md")


def main() -> None:
    old_files = [p.resolve() for folder in TOPICS.iterdir() if folder.is_dir()
                 for p in folder.glob("*.md") if p.name != "index.md"]
    contents = {p.resolve(): p.read_text(encoding="utf-8") for p in DOCS.rglob("*.md")}
    moves: dict[Path, Path] = {}
    groups: dict[str, dict[str, list[Path]]] = defaultdict(lambda: defaultdict(list))
    for old in old_files:
        topic = old.parent.name
        match = re.match(r"\A---\n(.*?)\n---\n", contents[old], re.S)
        if not match:
            raise SystemExit(f"Missing metadata: {old}")
        kind = (yaml.safe_load(match.group(1)) or {}).get("wiki_type", "")
        group = classify(topic, old.name, kind)
        new = old.parent / group / old.name
        moves[old] = new
        groups[topic][group].append(new)
    if len(set(moves.values())) != len(moves) or any(p.exists() for p in moves.values()):
        raise SystemExit("Target filename collision")

    for old, content in contents.items():
        new = moves.get(old, old)
        updated = markdown_links(content, old, new, moves)
        if old == (TOPICS / old.parent.name / "index.md").resolve() and old.parent.name in groups:
            lines = ["## 二级目录", "", "按子领域浏览，文档类型见各篇的 `wiki_type` 元数据。", ""]
            for group, files in sorted(groups[old.parent.name].items()):
                url = quote(group, safe="") + "/index.md"
                lines.append(f"- [{group}]({url})（{len(files)} 篇）")
            lines += ["", ""]
            heading = re.search(r"(?m)^## ", updated)
            if heading:
                updated = updated[:heading.start()] + "\n".join(lines) + updated[heading.start():]
            else:
                updated += "\n" + "\n".join(lines)
        new.parent.mkdir(parents=True, exist_ok=True)
        new.write_text(updated, encoding="utf-8")

    for old in moves:
        old.unlink()
    for topic, subgroups in groups.items():
        for group, files in subgroups.items():
            dest = TOPICS / topic / group / "index.md"
            lines = [
                "---",
                f"title: {json.dumps(group, ensure_ascii=False)}",
                "created: 2026-10-16",
                "updated: 2026-10-16",
                "tags: [llm-wiki, index]",
                "source: []",
                f"topic: {json.dumps(topic, ensure_ascii=False)}",
                "wiki_type: subtopic",
                "review_status: structural",
                "---",
                f"# {group}",
                "",
                f"返回[{topic}](../index.md)。本目录按主题聚合文章，具体文档类型见各篇元数据。",
                "",
            ]
            for page in sorted(files, key=lambda p: p.name):
                label = title_of(contents[next(old for old, new in moves.items() if new == page)], page.name)
                lines.append(f"- [{label}]({quote(page.name, safe='-._~')})")
            dest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    migration = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    migration["mapping"] = {
        old: moves.get((DOCS / new).resolve(), (DOCS / new).resolve()).relative_to(DOCS.resolve()).as_posix()
        for old, new in migration["mapping"].items()
    }
    MAP_PATH.write_text(json.dumps(migration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    html = NOT_FOUND.read_text(encoding="utf-8")
    old_redirect = json.loads(re.search(r"(?m)^const oldToNew=(.*);$", html).group(1))
    paths = {old.relative_to(DOCS).with_suffix("").as_posix():
             new.relative_to(DOCS).with_suffix("").as_posix() for old, new in moves.items()}
    redirect = {old: paths.get(new, new) for old, new in old_redirect.items()}
    redirect.update(paths)
    payload = json.dumps(redirect, ensure_ascii=False, separators=(",", ":"))
    html = re.sub(r"(?m)^const oldToNew=.*;$", "const oldToNew=" + payload + ";", html)
    NOT_FOUND.write_text(html, encoding="utf-8")
    print(f"Moved {len(moves)} articles into {sum(map(len, groups.values()))} subject directories")
    for topic, subgroups in sorted(groups.items()):
        print(topic + ": " + ", ".join(f"{name} {len(files)}" for name, files in sorted(subgroups.items())))


if __name__ == "__main__":
    main()
