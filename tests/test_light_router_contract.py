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

    def test_router_derives_first_static_chapter_from_manifest(self):
        router = self.router()
        self.assertIn('const staticNumbers = manifest.chapters', router)
        self.assertIn('const firstStatic = Math.min(...staticNumbers);', router)

    def test_router_fallback_is_limited_to_legacy_chapters(self):
        router = self.router()
        self.assertIn('if (requested >= firstStatic)', router)
        self.assertLess(router.index('if (requested >= firstStatic)'), router.index("script.src = 'assets/light-reader.js"))

    def test_router_rejects_static_manifest_holes_instead_of_masking_them(self):
        router = self.router()
        self.assertIn("location.replace('light/index.html');", router)
        self.assertIn('if (requested >= firstStatic)', router)

    def test_router_rejects_malformed_manifest_metadata(self):
        router = self.router()
        self.assertIn("if (!manifest || !Array.isArray(manifest.chapters))", router)
        self.assertIn('if (!Number.isInteger(latest) || staticNumbers.length === 0)', router)

    def test_frontier_verifier_requires_contiguous_text_manifest_range(self):
        verifier = (ROOT / 'scripts/verify_reader_frontier.py').read_text(encoding='utf-8')
        self.assertIn("Text manifest chapter range is not contiguous", verifier)
        self.assertIn('manifest_numbers = sorted(', verifier)


if __name__ == '__main__':
    unittest.main()
