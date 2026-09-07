#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA = "rehearsal_campaign_queue/v1"
SETTLED = {"applied", "source_win"}
VALID_STATUSES = {"pending", "running", "blocked", *SETTLED}
VALID_RESULTS = SETTLED


def build_batches(start: int, end: int, batch_size: int) -> list[tuple[int, int]]:
    if start < 1 or end < start or batch_size < 1:
        raise ValueError("invalid campaign range")
    out: list[tuple[int, int]] = []
    cursor = start
    while cursor <= end:
        batch_end = min(cursor + batch_size - 1, end)
        out.append((cursor, batch_end))
        cursor = batch_end + 1
    return out


def new_state(target_branch: str, start: int, end: int, batch_size: int) -> dict:
    state = {
        "schema": SCHEMA,
        "target_branch": target_branch,
        "start": start,
        "end": end,
        "batch_size": batch_size,
        "settled_authority": None,
        "batches": [
            {
                "start": a,
                "end": b,
                "status": "pending",
                "source_authority": None,
                "settled_authority": None,
                "retry_count": 0,
                "retryable": False,
                "blocking_reason": None,
                "manifest_path": None,
                "report_path": None,
                "validation": None,
            }
            for a, b in build_batches(start, end, batch_size)
        ],
    }
    validate_state(state)
    return state


def validate_state(state: dict) -> None:
    if state.get("schema") != SCHEMA:
        raise ValueError("invalid queue schema")
    target_branch = state.get("target_branch")
    if not isinstance(target_branch, str) or not target_branch:
        raise ValueError("target_branch is required")
    expected = build_batches(state.get("start"), state.get("end"), state.get("batch_size"))
    batches = state.get("batches")
    if not isinstance(batches, list) or len(batches) != len(expected):
        raise ValueError("queue batches do not match campaign range")

    saw_unsettled = False
    running_count = 0
    for batch, pair in zip(batches, expected):
        if (batch.get("start"), batch.get("end")) != pair:
            raise ValueError("queue batch ordering mismatch")
        status = batch.get("status")
        if status not in VALID_STATUSES:
            raise ValueError(f"invalid batch status: {status}")
        retry_count = batch.get("retry_count")
        if not isinstance(retry_count, int) or retry_count < 0 or retry_count > 1:
            raise ValueError("retry_count must be 0 or 1")
        if status == "running":
            running_count += 1
            if not batch.get("source_authority"):
                raise ValueError("running batch requires source authority")
        if status in SETTLED:
            if not batch.get("source_authority") or not batch.get("settled_authority"):
                raise ValueError("settled batch requires source and settled authority")
            if saw_unsettled:
                raise ValueError("settled batches cannot appear after an unsettled batch")
        else:
            saw_unsettled = True
        if status == "blocked" and not batch.get("blocking_reason"):
            raise ValueError("blocked batch requires blocking reason")
    if running_count > 1:
        raise ValueError("only one batch may be running")

    settled = [b for b in batches if b["status"] in SETTLED]
    expected_authority = settled[-1]["settled_authority"] if settled else None
    if state.get("settled_authority") != expected_authority:
        raise ValueError("queue settled_authority does not match last settled batch")


def current_unsettled(state: dict) -> dict | None:
    validate_state(state)
    for batch in state["batches"]:
        if batch["status"] not in SETTLED:
            return batch
    return None


def next_batch(state: dict) -> dict | None:
    batch = current_unsettled(state)
    if batch is None or batch["status"] != "pending":
        return None
    return batch


def claim_next(state: dict, source_authority: str) -> dict:
    if not isinstance(source_authority, str) or not source_authority:
        raise ValueError("source authority is required")
    current = current_unsettled(state)
    if current is None:
        raise ValueError("campaign is complete")
    if current["status"] == "running":
        raise ValueError("current batch is already running")
    if current["status"] == "blocked":
        raise ValueError("current batch is blocked")
    if current["status"] != "pending":
        raise ValueError("current batch is not claimable")
    if state["settled_authority"] and source_authority != state["settled_authority"]:
        raise ValueError("source authority must equal queue settled authority")
    current.update(
        status="running",
        source_authority=source_authority,
        settled_authority=None,
        retryable=False,
        blocking_reason=None,
        manifest_path=None,
        report_path=None,
        validation=None,
    )
    validate_state(state)
    return current


def settle_current(
    state: dict,
    source_authority: str,
    settled_authority: str,
    result: str,
    *,
    manifest_path: str | None = None,
    report_path: str | None = None,
    validation: str = "green",
) -> dict:
    if result not in VALID_RESULTS:
        raise ValueError("result must be applied or source_win")
    current = current_unsettled(state)
    if current is None or current["status"] != "running":
        raise ValueError("no running batch to settle")
    if current["source_authority"] != source_authority:
        raise ValueError("source authority does not match current claim")
    if not isinstance(settled_authority, str) or not settled_authority:
        raise ValueError("settled authority is required")
    current.update(
        status=result,
        settled_authority=settled_authority,
        manifest_path=manifest_path,
        report_path=report_path,
        validation=validation,
        retryable=False,
        blocking_reason=None,
    )
    state["settled_authority"] = settled_authority
    validate_state(state)
    return current


def block_current(state: dict, reason: str, *, retryable: bool = False) -> dict:
    current = current_unsettled(state)
    if current is None or current["status"] != "running":
        raise ValueError("no running batch to block")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("blocking reason is required")
    current.update(status="blocked", blocking_reason=reason.strip(), retryable=bool(retryable))
    validate_state(state)
    return current


def retry_current(state: dict, source_authority: str) -> dict:
    current = current_unsettled(state)
    if current is None or current["status"] != "blocked":
        raise ValueError("no blocked batch to retry")
    if not current.get("retryable"):
        raise ValueError("blocked batch is not retryable")
    if current["retry_count"] >= 1:
        raise ValueError("retry limit exceeded")
    if current["source_authority"] != source_authority:
        raise ValueError("source authority does not match blocked claim")
    current.update(
        status="running",
        retry_count=current["retry_count"] + 1,
        retryable=False,
        blocking_reason=None,
    )
    validate_state(state)
    return current


def load_state(path: str | Path) -> dict:
    state = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_state(state)
    return state


def save_state(path: str | Path, state: dict) -> None:
    validate_state(state)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage the serial REHEARSAL campaign queue.")
    parser.add_argument("state")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    claim = sub.add_parser("claim")
    claim.add_argument("--source-authority", required=True)
    settle = sub.add_parser("settle")
    settle.add_argument("--source-authority", required=True)
    settle.add_argument("--settled-authority", required=True)
    settle.add_argument("--result", choices=sorted(VALID_RESULTS), required=True)
    settle.add_argument("--manifest-path")
    settle.add_argument("--report-path")
    block = sub.add_parser("block")
    block.add_argument("--reason", required=True)
    block.add_argument("--retryable", action="store_true")
    retry = sub.add_parser("retry")
    retry.add_argument("--source-authority", required=True)
    args = parser.parse_args()

    path = Path(args.state)
    state = load_state(path)
    result = None
    if args.command == "status":
        result = {"settled_authority": state["settled_authority"], "next": current_unsettled(state)}
    elif args.command == "claim":
        result = claim_next(state, args.source_authority)
        save_state(path, state)
    elif args.command == "settle":
        result = settle_current(
            state,
            args.source_authority,
            args.settled_authority,
            args.result,
            manifest_path=args.manifest_path,
            report_path=args.report_path,
        )
        save_state(path, state)
    elif args.command == "block":
        result = block_current(state, args.reason, retryable=args.retryable)
        save_state(path, state)
    elif args.command == "retry":
        result = retry_current(state, args.source_authority)
        save_state(path, state)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
