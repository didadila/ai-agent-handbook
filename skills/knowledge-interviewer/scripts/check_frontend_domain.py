#!/usr/bin/env python3
"""Check frontend knowledge coverage, dependencies, references and legacy IDs."""
from __future__ import annotations

import argparse
import datetime as dt
import re
from collections import Counter
from pathlib import Path
from zoneinfo import ZoneInfo

ID = r"fe\.[a-z0-9_.-]+"
PLANNED = {
    "fe.js.async", "fe.ts.contract", "fe.web.lifecycle", "fe.state.task",
    "fe.stream.recovery", "fe.security.output", "fe.approval.scope",
    "fe.render.react", "fe.perf.streaming", "fe.a11y.status",
    "fe.quality.delivery", "fe.eval.journey", "fe.product.artifact",
}
SIX = ("结论", "案例", "机制", "误解靶子", "判据", "自测题")


def table_ids(text: str, cells: int) -> list[str]:
    result = []
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) == cells and re.fullmatch(rf"`({ID})`", parts[0]):
            result.append(parts[0].strip("`"))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--progress", type=Path,
                        default=Path(__file__).resolve().parents[3] / ".local/learning/frontend/progress.md")
    args = parser.parse_args()
    skill = Path(__file__).resolve().parents[1]
    root = skill.parents[1]
    domain = skill / "references/domains/frontend"
    book = root / "handbook/frontend"
    errors = []
    map_text = (domain / "map.md").read_text()
    questions = (domain / "questions.md").read_text()
    sources = (domain / "sources.md").read_text()
    ids = table_ids(map_text, 5)
    qids = re.findall(rf"^### `({ID})`", questions, re.M)
    source_ids = table_ids(sources, 4)
    chapters = sorted(book.glob("0[1-7]-*.md"))
    bodies = []
    for path in chapters:
        sections = re.split(rf"^## ({ID})[^\n]*\n", path.read_text(), flags=re.M)
        for index in range(1, len(sections), 2):
            name, body = sections[index:index + 2]
            bodies.append(name)
            if tuple(re.findall(r"^### (.+)$", body, re.M)) != SIX:
                errors.append(f"{path.name}: {name} must contain the six teaching sections")
    for label, values in (("map", ids), ("questions", qids),
                          ("sources", source_ids), ("book", bodies)):
        duplicates = [key for key, count in Counter(values).items() if count > 1]
        if duplicates:
            errors.append(f"{label} duplicate IDs: {duplicates}")
        if set(values) != set(ids):
            errors.append(f"{label} coverage differs: {sorted(set(values) ^ set(ids))}")
    if len(ids) != 19 or len(chapters) != 7:
        errors.append(f"expected 19 points and 7 chapters, got {len(ids)} and {len(chapters)}")
    if not PLANNED <= set(ids):
        errors.append(f"original planned IDs missing: {sorted(PLANNED - set(ids))}")
    for index, section in enumerate(re.split(rf"^### `({ID})`[^\n]*\n", questions, flags=re.M)):
        # Odd parts contain IDs, even nonzero parts contain their question chain.
        if index > 0 and index % 2 == 0:
            for field in ("首题", "追问链", "A 档要点", "错误答法识别", "最小验证"):
                if f"**{field}**" not in section:
                    errors.append(f"question chain missing: {field}")
    dependencies = map_text.split("## 直接依赖", 1)[1].split("## 组题", 1)[0]
    graph = {name: [] for name in ids}
    for line in dependencies.splitlines():
        found = re.findall(rf"`({ID})`", line)
        if found:
            graph[found[0]] = found[1:]
    visiting, visited = set(), set()

    def visit(name: str) -> None:
        if name not in graph:
            errors.append(f"unknown prerequisite: {name}")
        elif name in visiting:
            errors.append(f"dependency cycle: {name}")
        elif name not in visited:
            visiting.add(name)
            for dependency in graph[name]:
                visit(dependency)
            visiting.remove(name)
            visited.add(name)

    for name in graph:
        visit(name)
    declared = set(re.findall(r"^\- \*\*\[F(\d+)\]\*\*", sources, re.M))
    used = set(re.findall(r"\[F(\d+)\]", sources))
    if used - declared or not {str(number) for number in range(1, 34)} <= declared:
        errors.append("source anchors missing or an original F1-F33 source was removed")
    match = re.search(r"verified_at: (\d{4}-\d{2}-\d{2})", sources)
    if not match:
        errors.append("missing source verification date")
    else:
        age = (dt.datetime.now(ZoneInfo("Asia/Shanghai")).date() -
               dt.date.fromisoformat(match[1])).days
        if not 0 <= age <= 14:
            errors.append(f"source date out of freshness range: {age} days")
    checked = [*book.rglob("*.md"), *domain.glob("*.md"), skill / "SKILL.md",
               root / "README.md", root / "handbook/README.md", root / "skills/README.md"]
    for path in checked:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            if not (path.parent / target.split("#")[0]).exists():
                errors.append(f"broken link in {path.relative_to(root)}: {target}")
    entrypoint = (skill / "SKILL.md").read_text()
    for resource in ("map.md", "questions.md", "sources.md", "maintenance.md"):
        if f"references/domains/frontend/{resource}" not in entrypoint:
            errors.append(f"frontend resource not discoverable from Skill: {resource}")
    if args.progress.exists():
        previous = set(re.findall(r"\b(fe\.[a-z0-9_]+(?:\.[a-z0-9_-]+)+)\b",
                                  args.progress.read_text()))
        if previous - set(ids):
            errors.append(f"legacy progress IDs missing: {sorted(previous - set(ids))}")
        progress_note = f"legacy IDs: {len(previous)}"
    else:
        progress_note = "no learner profile; no grades created"
    if errors:
        print("FAIL\n" + "\n".join(errors))
        return 1
    print(f"PASS: {len(ids)} IDs, {len(chapters)} chapters, {len(qids)} question chains, "
          f"{len(declared)} sources; dependencies and local links valid; {progress_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
