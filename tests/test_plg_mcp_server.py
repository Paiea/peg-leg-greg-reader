import asyncio
import unittest

from scripts import plg_ai_tools
from scripts import plg_mcp_server


class PLGMCPServerTests(unittest.TestCase):
    def test_adapter_exposes_same_tool_names(self):
        self.assertEqual(set(plg_ai_tools.TOOLS), set(plg_mcp_server.TOOL_NAMES))

    def test_mcp_dependency_is_optional_for_module_import(self):
        self.assertIsInstance(plg_mcp_server.mcp_available(), bool)

    def test_build_server_lists_all_tools_when_sdk_is_installed(self):
        if not plg_mcp_server.mcp_available():
            self.skipTest("optional MCP SDK is not installed")
        server = plg_mcp_server.build_server()
        tools = asyncio.run(server.list_tools())
        self.assertEqual(set(plg_ai_tools.TOOLS), {tool.name for tool in tools})
        by_name = {tool.name: tool for tool in tools}
        self.assertFalse(by_name["apply_survivors"].annotations.read_only_hint)
        self.assertTrue(by_name["apply_survivors"].annotations.destructive_hint)
        self.assertTrue(by_name["get_scene_view"].annotations.read_only_hint)


if __name__ == "__main__":
    unittest.main()
