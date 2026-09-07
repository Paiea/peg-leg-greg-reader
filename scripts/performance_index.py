#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3
from typing import Any


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _claim_value(value: object) -> object:
    if isinstance(value, dict) and "value" in value:
        return value.get("value")
    return value


def _flatten_text(value: object) -> list[str]:
    value = _claim_value(value)
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (int, float, bool)):
        return [str(value)]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(_flatten_text(item))
        return result
    if isinstance(value, dict):
        result = []
        for item in value.values():
            result.extend(_flatten_text(item))
        return result
    return []


def _scene_row(record: dict[str, Any]) -> tuple[Any, ...]:
    scene_id = str(record.get("scene_id", ""))
    source = record.get("source") if isinstance(record.get("source"), dict) else {}
    mechanical = record.get("mechanical") if isinstance(record.get("mechanical"), dict) else {}
    semantic = record.get("semantic") if isinstance(record.get("semantic"), dict) else {}
    comparison = record.get("comparison") if isinstance(record.get("comparison"), dict) else {}
    chapter = source.get("chapter")
    if not isinstance(chapter, int):
        try:
            chapter = int(scene_id.split(".", 1)[0])
        except (ValueError, IndexError):
            chapter = 0
    paragraphs = source.get("paragraphs") if isinstance(source.get("paragraphs"), list) else []
    source_text = "\n".join(str(p) for p in paragraphs)
    semantic_text = "\n".join(_flatten_text(semantic))
    tokens = mechanical.get("capitalized_tokens") if isinstance(mechanical.get("capitalized_tokens"), list) else []
    money = mechanical.get("money_mentions") if isinstance(mechanical.get("money_mentions"), list) else []
    conflicts = record.get("semantic_conflicts") if isinstance(record.get("semantic_conflicts"), list) else []
    span = source.get("paragraph_span") if isinstance(source.get("paragraph_span"), list) else []
    return (
        scene_id,
        chapter,
        str(source.get("hash", "")),
        json.dumps(span, ensure_ascii=False),
        str(source.get("start_anchor", "")),
        str(source.get("end_anchor", "")),
        int(mechanical.get("dialogue_turns", 0) or 0),
        float(mechanical.get("dialogue_ratio", 0.0) or 0.0),
        int(mechanical.get("question_count", 0) or 0),
        int(mechanical.get("action_word_hits", 0) or 0),
        json.dumps(tokens, ensure_ascii=False),
        "\n".join(str(token) for token in tokens),
        json.dumps(money, ensure_ascii=False),
        "\n".join(str(item) for item in money),
        str(comparison.get("verdict", "")),
        1 if conflicts else 0,
        1 if isinstance(record.get("performance"), dict) else 0,
        1 if isinstance(record.get("screenplay"), dict) else 0,
        source_text,
        semantic_text,
    )


def _connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def rebuild_index(compiled_root: Path, db_path: Path) -> dict[str, Any]:
    compiled_root = Path(compiled_root)
    db_path = Path(db_path)
    if db_path.exists():
        db_path.unlink()
    conn = _connect(db_path)
    try:
        conn.executescript(
            """
            PRAGMA journal_mode=WAL;
            CREATE TABLE scenes (
                scene_id TEXT PRIMARY KEY,
                chapter INTEGER NOT NULL,
                source_hash TEXT NOT NULL,
                paragraph_span_json TEXT NOT NULL,
                start_anchor TEXT NOT NULL,
                end_anchor TEXT NOT NULL,
                dialogue_turns INTEGER NOT NULL,
                dialogue_ratio REAL NOT NULL,
                question_count INTEGER NOT NULL,
                action_word_hits INTEGER NOT NULL,
                tokens_json TEXT NOT NULL,
                tokens_text TEXT NOT NULL,
                money_json TEXT NOT NULL,
                money_text TEXT NOT NULL,
                comparison_verdict TEXT NOT NULL,
                has_conflict INTEGER NOT NULL,
                has_performance INTEGER NOT NULL,
                has_screenplay INTEGER NOT NULL,
                source_text TEXT NOT NULL,
                semantic_text TEXT NOT NULL
            );
            CREATE INDEX scenes_chapter_idx ON scenes(chapter);
            CREATE INDEX scenes_verdict_idx ON scenes(comparison_verdict);
            CREATE VIRTUAL TABLE scenes_fts USING fts5(scene_id UNINDEXED, source_text, semantic_text, tokens_text, money_text);
            """
        )
        scene_count = 0
        for path in sorted(compiled_root.glob("[0-9][0-9][0-9]/s*.json")):
            record = _read_json(path)
            if not record or not isinstance(record.get("scene_id"), str):
                continue
            row = _scene_row(record)
            conn.execute(
                """INSERT INTO scenes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                row,
            )
            conn.execute(
                "INSERT INTO scenes_fts(scene_id, source_text, semantic_text, tokens_text, money_text) VALUES (?,?,?,?,?)",
                (row[0], row[18], row[19], row[11], row[13]),
            )
            scene_count += 1
        conn.commit()
        return {"scene_count": scene_count, "db_path": db_path.as_posix()}
    finally:
        conn.close()


def _decode_row(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "scene_id": row["scene_id"],
        "chapter": row["chapter"],
        "source_hash": row["source_hash"],
        "paragraph_span": json.loads(row["paragraph_span_json"]),
        "start_anchor": row["start_anchor"],
        "end_anchor": row["end_anchor"],
        "dialogue_turns": row["dialogue_turns"],
        "dialogue_ratio": row["dialogue_ratio"],
        "question_count": row["question_count"],
        "action_word_hits": row["action_word_hits"],
        "tokens": json.loads(row["tokens_json"]),
        "money_mentions": json.loads(row["money_json"]),
        "comparison_verdict": row["comparison_verdict"] or None,
        "has_conflict": bool(row["has_conflict"]),
        "has_performance": bool(row["has_performance"]),
        "has_screenplay": bool(row["has_screenplay"]),
    }


def query_scenes(
    db_path: Path,
    *,
    query: str | None = None,
    scene_id: str | None = None,
    chapter_start: int | None = None,
    chapter_end: int | None = None,
    token: str | None = None,
    money: str | None = None,
    verdict: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    if limit < 1 or limit > 1000:
        raise ValueError("limit must be between 1 and 1000")
    conn = _connect(Path(db_path))
    try:
        clauses: list[str] = []
        params: list[Any] = []
        join = ""
        if query:
            join = " JOIN scenes_fts ON scenes_fts.scene_id = scenes.scene_id"
            clauses.append("scenes_fts MATCH ?")
            params.append(query)
        if scene_id:
            clauses.append("scenes.scene_id = ?")
            params.append(scene_id)
        if chapter_start is not None:
            clauses.append("scenes.chapter >= ?")
            params.append(chapter_start)
        if chapter_end is not None:
            clauses.append("scenes.chapter <= ?")
            params.append(chapter_end)
        if token:
            clauses.append("lower(scenes.tokens_text) LIKE ?")
            params.append(f"%{token.lower()}%")
        if money:
            clauses.append("lower(scenes.money_text) LIKE ?")
            params.append(f"%{money.lower()}%")
        if verdict:
            clauses.append("scenes.comparison_verdict = ?")
            params.append(verdict)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"SELECT scenes.* FROM scenes{join}{where} ORDER BY scenes.chapter, scenes.scene_id LIMIT ?"
        params.append(limit)
        try:
            rows = conn.execute(sql, params).fetchall()
        except sqlite3.OperationalError as exc:
            if query and "fts5" not in str(exc).lower():
                fallback_clauses = [clause for clause in clauses if clause != "scenes_fts MATCH ?"]
                fallback_params = params[:-1]
                if query in fallback_params:
                    fallback_params.remove(query)
                fallback_clauses.append("lower(scenes.source_text || ' ' || scenes.semantic_text || ' ' || scenes.tokens_text || ' ' || scenes.money_text) LIKE ?")
                fallback_params.append(f"%{query.lower()}%")
                fallback_params.append(limit)
                fallback_where = f" WHERE {' AND '.join(fallback_clauses)}"
                rows = conn.execute(f"SELECT scenes.* FROM scenes{fallback_where} ORDER BY scenes.chapter, scenes.scene_id LIMIT ?", fallback_params).fetchall()
            else:
                raise
        return [_decode_row(row) for row in rows]
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild or query the disposable PLG PERFORMANCE scene index.")
    sub = parser.add_subparsers(dest="command", required=True)
    rebuild = sub.add_parser("rebuild")
    rebuild.add_argument("--compiled-root", type=Path, required=True)
    rebuild.add_argument("--db", type=Path, required=True)
    query_cmd = sub.add_parser("query")
    query_cmd.add_argument("--db", type=Path, required=True)
    query_cmd.add_argument("--query")
    query_cmd.add_argument("--scene")
    query_cmd.add_argument("--chapter-start", type=int)
    query_cmd.add_argument("--chapter-end", type=int)
    query_cmd.add_argument("--token")
    query_cmd.add_argument("--money")
    query_cmd.add_argument("--verdict")
    query_cmd.add_argument("--limit", type=int, default=50)
    args = parser.parse_args(argv)
    if args.command == "rebuild":
        result = rebuild_index(args.compiled_root, args.db)
    else:
        result = query_scenes(
            args.db,
            query=args.query,
            scene_id=args.scene,
            chapter_start=args.chapter_start,
            chapter_end=args.chapter_end,
            token=args.token,
            money=args.money,
            verdict=args.verdict,
            limit=args.limit,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
