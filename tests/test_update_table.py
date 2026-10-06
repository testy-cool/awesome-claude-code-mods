import importlib.util
from pathlib import Path
import unittest


script = Path(__file__).resolve().parents[1] / "scripts" / "update-table.py"
spec = importlib.util.spec_from_file_location("update_table", script)
table = importlib.util.module_from_spec(spec)
spec.loader.exec_module(table)


class SourceRepositoryTests(unittest.TestCase):
    def test_existing_github_source_keeps_its_repository(self):
        self.assertEqual(table.repo_from_source({"source": "github", "repo": "NovusEdge/glowup"}), "NovusEdge/glowup")

    def test_nested_plugin_git_url_becomes_the_repository_api_path(self):
        source = {"source": "git-subdir", "url": "https://github.com/416rehman/spinlings.git", "path": "plugin"}
        self.assertEqual(table.repo_from_source(source), "416rehman/spinlings")
        self.assertEqual("https://api.github.com/repos/" + table.repo_from_source(source), "https://api.github.com/repos/416rehman/spinlings")

    def test_non_github_and_nested_page_urls_are_rejected(self):
        for url in ["https://example.com/owner/repo", "https://github.com/owner/repo/tree/main/plugin"]:
            with self.assertRaises(ValueError):
                table.repo_from_source({"url": url})


if __name__ == "__main__":
    unittest.main()
