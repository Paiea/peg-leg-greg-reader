#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from typing import Any

from scripts import plg_ai_tools

TOOL_NAMES = tuple(plg_ai_tools.TOOLS)


def mcp_available() -> bool:
    return importlib.util.find_spec("mcp") is not None


def build_server():
    if not mcp_available():
        raise RuntimeError("MCP support is optional. Install it with: pip install -r requirements-mcp.txt")
    from mcp.server import MCPServer
    from mcp.types import ToolAnnotations

    server = MCPServer("Peg-Leg Greg AI Tools")

    def register(name: str) -> None:
        spec = plg_ai_tools.TOOL_SPECS[name]
        canon_write = bool(spec.get("write"))
        read_only = bool(spec.get("read_only", not canon_write))

        def invoke(payload: dict[str, Any]) -> Any:
            return plg_ai_tools.call_tool(name, payload)

        invoke.__name__ = f"plg_{name}"
        invoke.__doc__ = str(spec.get("description", name))
        annotations = ToolAnnotations(
            readOnlyHint=read_only,
            destructiveHint=canon_write,
            idempotentHint=read_only,
            openWorldHint=False,
        )
        server.tool(
            name=name,
            description=str(spec.get("description", name)),
            annotations=annotations,
        )(invoke)

    for tool_name in TOOL_NAMES:
        register(tool_name)
    return server


def main() -> int:
    server = build_server()
    server.run("stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
