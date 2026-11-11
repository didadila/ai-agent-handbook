#!/usr/bin/env python3
"""Static checks for the knowledge-interviewer AI Agent domain."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from collections import Counter
from pathlib import Path

ID_RE = re.compile(r"\b(agent\.[a-z0-9_]+(?:\.[a-z0-9_-]+)+)\b")
MAP_ROW_RE = re.compile(r"^\|\s*`(agent\.[a-z0-9_.-]+)`\s*\|", re.MULTILINE)
QUESTION_RE = re.compile(r"^###\s+`(agent\.[a-z0-9_.-]+)`", re.MULTILINE)
SOURCE_REF_RE = re.compile(r"\[S(\d+)\]")
SOURCE_DECL_RE = re.compile(r"^\s*-\s+\*\*\[S(\d+)\]\*\*", re.MULTILINE)
DATE_RE = re.compile(r"verified_at:\s*(\d{4}-\d{2}-\d{2})")

REQUIRED_IDS = {
    "agent.arch.workflow",
    "agent.runtime.durable",
    "agent.protocol.interop",
    "agent.ctx.memory",
    "agent.tool.protocol",
    "agent.rag.evaluation",
    "agent.eval.design",
    "agent.fail.observability",
    "agent.cost.latency",
    "agent.safety.boundary",
}


def duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--progress", type=Path, default=Path(__file__).resolve().parents[3] / ".local/learning/ai-agent/progress.md")
    parser.add_argument("--max-source-age-days", type=int, default=14)
    args = parser.parse_args()

    domain = Path(__file__).resolve().parents[1] / "references/domains/ai-agent"
    map_text = (domain / "map.md").read_text(encoding="utf-8")
    questions_text = (domain / "questions.md").read_text(encoding="utf-8")
    sources_text = (domain / "sources.md").read_text(encoding="utf-8")

    errors: list[str] = []
    notes: list[str] = []

    map_ids_list = MAP_ROW_RE.findall(map_text)
    question_ids_list = QUESTION_RE.findall(questions_text)
    map_ids = set(map_ids_list)
    question_ids = set(question_ids_list)

    for duplicate in duplicates(map_ids_list):
        errors.append(f"duplicate map id: {duplicate}")
    for duplicate in duplicates(question_ids_list):
        errors.append(f"duplicate question id: {duplicate}")

    unknown_questions = sorted(question_ids - map_ids)
    if unknown_questions:
        errors.append("question ids missing from map: " + ", ".join(unknown_questions))

    missing_required = sorted(REQUIRED_IDS - map_ids)
    if missing_required:
        errors.append("required ids missing: " + ", ".join(missing_required))

    declared_sources = set(SOURCE_DECL_RE.findall(sources_text))
    used_sources = set(SOURCE_REF_RE.findall(sources_text))
    missing_sources = sorted(used_sources - declared_sources, key=int)
    if missing_sources:
        errors.append("source references not declared: " + ", ".join(f"S{x}" for x in missing_sources))

    date_match = DATE_RE.search(sources_text)
    if not date_match:
        errors.append("sources.md has no verified_at ISO date")
    else:
        verified = dt.date.fromisoformat(date_match.group(1))
        age = (dt.date.today() - verified).days
        if age < 0:
            errors.append(f"verified_at is in the future: {verified}")
        elif age > args.max_source_age_days:
            errors.append(f"sources are stale: {age} days > {args.max_source_age_days}")
        else:
            notes.append(f"sources age: {age} days")

    if args.progress.exists():
        progress_ids = set(ID_RE.findall(args.progress.read_text(encoding="utf-8")))
        missing_progress_ids = sorted(progress_ids - map_ids)
        if missing_progress_ids:
            errors.append("legacy progress ids missing from map: " + ", ".join(missing_progress_ids))
        else:
            notes.append(f"legacy progress compatibility: {len(progress_ids)} ids")
    else:
        notes.append("progress file absent; compatibility check skipped")

    notes.extend([
        f"map ids: {len(map_ids)}",
        f"question chains: {len(question_ids)}",
        f"declared sources: {len(declared_sources)}",
    ])

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        for note in notes:
            print(f"- note: {note}")
        return 1

    print("PASS")
    for note in notes:
        print(f"- {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
