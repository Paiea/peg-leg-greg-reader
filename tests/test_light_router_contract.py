import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LightRouterContractTests(unittest.TestCase):
    def router(self) -> str:
        return (ROOT / 'light.html').read_text(encoding='utf-8')

    def test_router_requires_strict_integer_query_parameter(self):
        router = self.router()
        self.assertIn("const requested = Number(params.get('chapter') || '');", router)
        self.assertNotIn("Number.parseInt(params.get('chapter')", router)

    def test_router_rejects_invalid_requests_before_manifest_routing(self):
        router = self.router()
        self.assertIn('if (!Number.isInteger(requested) || requested < 1)', router)
        self.assertIn("location.replace('light/index.html')", router)

    def test_router_rejects_requests_beyond_manifest_frontier(self):
        router = self.router()
        self.assertIn('const latest = Number(manifest?.latest);', router)
        self.assertIn('Number.isInteger(latest)', router)
        self.assertIn('requested > latest', router)

    def test_router_only_trusts_exact_manifest_path_for_requested_chapter(self):
        router = self.router()
        self.assertIn("const expectedPath = `${String(requested).padStart(3, '0')}.html`;", router)
        self.assertIn('found?.path === expectedPath', router)

    def test_router_loads_fallback_only_for_valid_in_range_manifest_miss(self):
        router = self.router()
        self.assertIn('if (found?.path === expectedPath)', router)
        self.assertIn("script.src = 'assets/light-reader.js", router)
        self.assertLess(router.index('requested > latest'), router.index("script.src = 'assets/light-reader.js"))


if __name__ == '__main__':
    unittest.main()
