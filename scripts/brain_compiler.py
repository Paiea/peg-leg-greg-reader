#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import re
from pathlib import Path
from typing import Any

SCHEMA = "plg_brain_routing/v1"
PACKET_SCHEMA = "plg_brain_packet/v1"
SNAPSHOT_SCHEMA = "plg_brain_github_snapshot/v1"
ALLOWED_TEMPERATURES = {"hot", "conditional", "cold"}
ALLOWED_WORKSTREAM_STATUS = {"ACTIVE", "VERIFIED", "FAILED", "SUPERSEDED", "ARCHIVAL"}
HARD_HOT_LIMIT = 12


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _norm(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value.lower()).split())


def load_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA:
        raise ValueError(f"invalid brain registry schema: {data.get('schema')!r}")
    project = data.get("project")
    required = {"authority", "canon", "root_router", "project_state", "manuscript_owner", "engines"}
    if not isinstance(project, dict) or not required <= set(project):
        raise ValueError("brain registry missing required project keys")
    docs = data.get("documents")
    if not isinstance(docs, list):
        raise ValueError("brain registry documents must be a list")
    paths: set[str] = set()
    by_path: dict[str, dict[str, Any]] = {}
    for row in docs:
        if not isinstance(row, dict):
            raise ValueError("brain registry document must be an object")
        for key in ("path", "owner", "authority_class", "default_temperature", "task_tags", "reason"):
            if key not in row:
                raise ValueError(f"brain registry document missing {key}")
        p = str(row["path"])
        if p in paths:
            raise ValueError(f"duplicate brain registry path: {p}")
        paths.add(p); by_path[p] = row
        if row["default_temperature"] not in ALLOWED_TEMPERATURES:
            raise ValueError(f"invalid temperature for {p}")
        if not isinstance(row.get("task_tags"), list):
            raise ValueError(f"task_tags must be a list for {p}")
    for ws in data.get("workstreams", []):
        if ws.get("status") not in ALLOWED_WORKSTREAM_STATUS:
            raise ValueError(f"invalid workstream status: {ws.get('id')}")
    graph: dict[str, list[str]] = {p: [] for p in paths}
    for p, row in by_path.items():
        for dep in row.get("dependencies", []):
            target = dep.get("path")
            temp = dep.get("temperature")
            if target not in by_path:
                raise ValueError(f"unregistered dependency {target} from {p}")
            if temp not in {"hot", "conditional"}:
                raise ValueError(f"invalid dependency temperature from {p} to {target}")
            graph[p].append(target)
    visiting: set[str] = set(); visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting: raise ValueError(f"circular brain dependency at {node}")
        if node in visited: return
        visiting.add(node)
        for nxt in graph[node]: visit(nxt)
        visiting.remove(node); visited.add(node)
    for p in sorted(graph): visit(p)
    return data


def _match_tags(task: str, registry: dict[str, Any]) -> list[str]:
    text = _norm(task)
    matched: set[str] = set()
    aliases = registry.get("tag_aliases", {})
    for alias, tags in aliases.items():
        if _norm(alias) in text:
            matched.update(map(str, tags))
    all_tags = {str(tag) for row in registry.get("documents", []) for tag in row.get("task_tags", [])}
    all_tags |= {str(tag) for ws in registry.get("workstreams", []) for tag in ws.get("task_tags", [])}
    for tag in all_tags:
        nt = _norm(tag)
        if nt and re.search(rf"(?:^| ){re.escape(nt)}(?: |$)", text):
            matched.add(tag)
    return sorted(matched)


def _pointer(row: dict[str, Any], source: str = "registry") -> dict[str, Any]:
    return {"path": str(row["path"]), "owner": str(row["owner"]), "reason": str(row["reason"]), "source": source}


def _workstream_row(ws: dict[str, Any], source: str = "registry") -> dict[str, Any]:
    out = {"id": str(ws["id"]), "status": str(ws["status"]), "reason": str(ws.get("reason", "")), "source": source}
    for key in ("owner_path", "branch", "accepted_commit", "pr"):
        if ws.get(key) is not None: out[key] = ws[key]
    return out


def compile_brain(task: str, repo_root: Path, registry_path: Path, authority_branch: str | None = None, authority_sha: str | None = None, github_snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    registry = load_registry(registry_path)
    project = registry["project"]
    matched = _match_tags(task, registry)
    warnings: list[dict[str, Any]] = []
    branch = authority_branch or str(project["authority"])
    snapshot_state = "absent"
    if github_snapshot is not None:
        if github_snapshot.get("schema") != SNAPSHOT_SCHEMA:
            raise ValueError("invalid GitHub snapshot schema")
        snapshot_state = "present"
        snap_sha = github_snapshot.get("authority_sha")
        if authority_sha and snap_sha and authority_sha != snap_sha:
            warnings.append({"code":"authority_sha_conflict","message":"Explicit authority SHA disagrees with GitHub snapshot."})
        elif authority_sha is None and snap_sha:
            authority_sha = str(snap_sha)
    if authority_sha is None:
        warnings.append({"code":"authority_sha_absent","message":"Exact accepted authority SHA was not supplied."})

    docs = {str(row["path"]): row for row in registry["documents"]}
    effective: dict[str, str] = {}
    for path, row in docs.items():
        if row.get("universal"):
            effective[path] = "hot"
        elif row.get("case_law"):
            effective[path] = "cold"
        elif matched and set(map(str, row.get("task_tags", []))) & set(matched):
            effective[path] = "hot"
        else:
            effective[path] = str(row["default_temperature"])
    changed = True
    while changed:
        changed = False
        for path, row in docs.items():
            if effective.get(path) != "hot": continue
            for dep in row.get("dependencies", []):
                target = str(dep["path"]); target_temp = str(dep["temperature"])
                desired = "hot" if target_temp == "hot" else "conditional"
                current = effective[target]
                rank = {"cold":0,"conditional":1,"hot":2}
                if rank[desired] > rank[current]: effective[target] = desired; changed = True
    hot_paths = sorted([p for p,t in effective.items() if t == "hot"])
    if len(hot_paths) > HARD_HOT_LIMIT:
        raise ValueError(f"HOT pointer ceiling exceeded for task {task!r}: {len(hot_paths)} > {HARD_HOT_LIMIT}")
    conditional_paths = sorted([p for p,t in effective.items() if t == "conditional"])
    cold_paths = sorted([p for p,t in effective.items() if t == "cold"])

    relevant_ws: list[dict[str, Any]] = []
    cold_ws: list[dict[str, Any]] = []
    for ws in sorted(registry.get("workstreams", []), key=lambda x: str(x.get("id", ""))):
        relevant = bool(set(map(str, ws.get("task_tags", []))) & set(matched))
        if ws.get("status") == "ACTIVE" and relevant:
            relevant_ws.append(_workstream_row(ws))
        elif ws.get("status") == "VERIFIED" and relevant:
            relevant_ws.append(_workstream_row(ws))
        elif ws.get("status") in {"SUPERSEDED","FAILED","ARCHIVAL"}:
            cold_ws.append(_workstream_row(ws))

    if github_snapshot is not None:
        branches = {str(x.get("name")): x for x in github_snapshot.get("branches", [])}
        prs = github_snapshot.get("pull_requests", [])
        for ws in registry.get("workstreams", []):
            b = ws.get("branch")
            if b and ws.get("status") == "ACTIVE" and b not in branches:
                merged = any(pr.get("head") == b and pr.get("merged") for pr in prs)
                if merged:
                    warnings.append({"code":"workstream_status_conflict","workstream_id":ws.get("id"),"message":"Durable ACTIVE workstream appears merged in supplied snapshot."})

    packet = {
        "schema": PACKET_SCHEMA,
        "task": task,
        "authority": {"branch": branch, "sha": authority_sha, "canon": str(project["canon"])},
        "routing": {"matched_tags": matched, "confidence": "high" if matched else "low", "github_snapshot": snapshot_state},
        "project": [
            {"key":"root_router","path":str(project["root_router"])},
            {"key":"project_state","path":str(project["project_state"])},
            {"key":"manuscript_owner","path":str(project["manuscript_owner"])},
            {"key":"engines","value":list(project["engines"])},
        ],
        "hot": [_pointer(docs[p]) for p in hot_paths],
        "conditional": [_pointer(docs[p]) for p in conditional_paths[:12]],
        "conditional_total": len(conditional_paths),
        "active_wip": relevant_ws[:12],
        "active_wip_total": len(relevant_ws),
        "cold_case_law": ([_pointer(docs[p]) for p in cold_paths] + cold_ws)[:12],
        "cold_case_law_total": len(cold_paths) + len(cold_ws),
        "warnings": sorted(warnings, key=canonical_json),
    }
    return packet


def render_packet_text(packet: dict[str, Any]) -> str:
    lines = ["PROJECT", f"  authority: {packet['authority']['branch']} {packet['authority'].get('sha') or '(sha not supplied)'}", f"  canon: {packet['authority']['canon']}"]
    for row in packet["project"]:
        if "path" in row: lines.append(f"  {row['key']}: {row['path']}")
        elif "value" in row: lines.append(f"  {row['key']}: {' / '.join(map(str,row['value']))}")
    def section(name: str, rows: list[dict[str, Any]]) -> None:
        lines.append(""); lines.append(name)
        if not rows: lines.append("  (none)"); return
        for row in rows:
            label = row.get("path") or row.get("id")
            status = f" [{row['status']}]" if row.get("status") else ""
            lines.append(f"  {label}{status} - {row.get('reason','')}")
    section("HOT FOR THIS TASK", packet["hot"])
    section("CONDITIONAL", packet["conditional"])
    section("ACTIVE WIP", packet["active_wip"])
    section("COLD / CASE LAW", packet["cold_case_law"])
    if packet["warnings"]:
        lines.append(""); lines.append("WARNINGS")
        for w in packet["warnings"]: lines.append(f"  {w['code']}: {w['message']}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile a compact task-specific PLG brain packet.")
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("compile")
    c.add_argument("--task", required=True); c.add_argument("--repo-root", type=Path, default=Path(".")); c.add_argument("--registry", type=Path, default=Path("state/brain/ROUTING_REGISTRY.json")); c.add_argument("--authority-branch"); c.add_argument("--authority-sha"); c.add_argument("--github-snapshot", type=Path); c.add_argument("--format", choices=("json","text"), default="text")
    args = parser.parse_args(argv)
    snap = json.loads(args.github_snapshot.read_text(encoding="utf-8")) if args.github_snapshot else None
    packet = compile_brain(args.task, args.repo_root, args.registry, args.authority_branch, args.authority_sha, snap)
    print(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) if args.format == "json" else render_packet_text(packet), end="" if args.format == "text" else "\n")
    return 0

if __name__ == "__main__": raise SystemExit(main())
