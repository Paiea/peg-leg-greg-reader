#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path
from typing import Any

from scripts import brain_compiler

REPORT_SCHEMA = "plg_brain_doctor/v1"
KNOWN_TASKS = [
    "continue manuscript",
    "writers room development",
    "story control plot",
    "whole-manuscript dialogue pass",
    "structural compression",
    "reverse edit performance",
    "money continuity",
    "illustration reconciliation",
    "reader UI",
    "publishing integration",
    "campaign codex execution",
]


def _finding(code: str, message: str, **extra: Any) -> dict[str, Any]:
    out = {"code": code, "message": message}
    out.update(extra)
    return out


def _ignored(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pat) for pat in patterns)


def run_doctor(repo_root: Path, registry_path: Path, github_snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    registry = brain_compiler.load_registry(registry_path)
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    advisories: list[dict[str, Any]] = []
    docs = {str(r["path"]): r for r in registry["documents"]}

    for required in (registry["project"]["root_router"], registry["project"]["project_state"], registry["project"]["manuscript_owner"]):
        if not (repo_root / str(required)).exists():
            errors.append(_finding("missing_project_pointer", f"Required project pointer is missing: {required}", path=str(required)))
    for path, row in docs.items():
        full = repo_root / path
        if not full.exists():
            errors.append(_finding("missing_registered_path", f"Registered brain path is missing: {path}", path=path))
            continue
        if full.is_file() and full.stat().st_size > 100_000 and row.get("default_temperature") == "hot":
            advisories.append(_finding("oversized_hot_document", f"HOT document is larger than 100 KB: {path}", path=path))
        if row.get("case_law") or row.get("default_temperature") == "cold":
            try:
                text = full.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = ""
            if "NEXT_TASK" in text:
                warnings.append(_finding("cold_next_task", f"Cold/case-law document still contains NEXT_TASK: {path}", path=path))

    discovery = registry.get("discovery", {})
    includes = list(discovery.get("include_globs", [])); ignores = list(discovery.get("ignore_globs", []))
    found: set[str] = set()
    for pattern in includes:
        for p in repo_root.glob(pattern):
            if p.is_file():
                rel = p.relative_to(repo_root).as_posix()
                if not _ignored(rel, ignores): found.add(rel)
    for rel in sorted(found - set(docs))[:25]:
        advisories.append(_finding("unregistered_brain_file", f"Likely durable brain file is not registered: {rel}", path=rel))

    claims: dict[str, list[str]] = {}
    exclusive = set(map(str, registry.get("exclusive_task_tags", [])))
    for ws in registry.get("workstreams", []):
        if ws.get("status") != "ACTIVE": continue
        for tag in map(str, ws.get("owner_tags", [])):
            if tag in exclusive: claims.setdefault(tag, []).append(str(ws.get("id")))
    for tag, ids in sorted(claims.items()):
        if len(ids) > 1:
            errors.append(_finding("exclusive_owner_collision", f"Multiple ACTIVE workstreams claim exclusive owner tag {tag}: {', '.join(sorted(ids))}", owner_tag=tag, workstream_ids=sorted(ids)))

    if github_snapshot is not None:
        if github_snapshot.get("schema") != brain_compiler.SNAPSHOT_SCHEMA:
            errors.append(_finding("invalid_snapshot_schema", "GitHub snapshot schema is invalid."))
        else:
            branches = {str(x.get("name")): x for x in github_snapshot.get("branches", [])}
            prs = list(github_snapshot.get("pull_requests", []))
            for ws in registry.get("workstreams", []):
                branch = ws.get("branch")
                if not branch: continue
                merged = any(pr.get("head") == branch and pr.get("merged") for pr in prs)
                if ws.get("status") == "ACTIVE" and merged:
                    warnings.append(_finding("workstream_status_conflict", f"ACTIVE workstream {ws['id']} appears merged in supplied snapshot.", workstream_id=str(ws["id"])))
                if ws.get("status") == "ACTIVE" and branch not in branches and not merged:
                    warnings.append(_finding("stale_branch_pointer", f"ACTIVE workstream branch not present in supplied snapshot: {branch}", workstream_id=str(ws["id"]), branch=str(branch)))

    for task in KNOWN_TASKS:
        try:
            brain_compiler.compile_brain(task, repo_root, registry_path, authority_branch=str(registry["project"]["authority"]), authority_sha="doctor-fixture", github_snapshot=None)
        except ValueError as exc:
            if "HOT pointer ceiling" in str(exc):
                errors.append(_finding("hot_rule_explosion", str(exc), task=task))

    def sorted_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(rows, key=brain_compiler.canonical_json)
    errors = sorted_rows(errors); warnings = sorted_rows(warnings); advisories = sorted_rows(advisories)
    return {"schema":REPORT_SCHEMA,"errors":errors,"warnings":warnings,"advisories":advisories,"counts":{"errors":len(errors),"warnings":len(warnings),"advisories":len(advisories)}}


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description="Validate PLG Brain routing health without modifying the repository.")
    sub=parser.add_subparsers(dest="command",required=True); c=sub.add_parser("check"); c.add_argument("--repo-root",type=Path,default=Path(".")); c.add_argument("--registry",type=Path,default=Path("state/brain/ROUTING_REGISTRY.json")); c.add_argument("--github-snapshot",type=Path)
    args=parser.parse_args(argv); snap=json.loads(args.github_snapshot.read_text(encoding="utf-8")) if args.github_snapshot else None
    report=run_doctor(args.repo_root,args.registry,snap); print(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)); return 1 if report["errors"] else 0

if __name__=="__main__": raise SystemExit(main())
