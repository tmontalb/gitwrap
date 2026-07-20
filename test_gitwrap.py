import unittest
import yaml

from gitwrap import to_yaml


class TestGitWrapUtility(unittest.TestCase):

    def test_yaml_serialization_basic(self):
        """Validates that a basic dictionary serializes to valid YAML."""
        data = {
            "action": "status",
            "branch": "main",
            "favourite_pokemon": "Pikachu"
        }

        output = to_yaml(data)

        self.assertEqual(
            yaml.safe_load(output),
            data
        )

    def test_yaml_serialization_booleans(self):
        """Validates boolean serialization."""
        data = {
            "dry_run": True,
            "action": "clean"
        }

        output = to_yaml(data)

        self.assertEqual(
            yaml.safe_load(output),
            data
        )

    def test_yaml_collections_omissions(self):
        """Empty lists and None values should be omitted."""
        data = {
            "action": "status",
            "staged_files": ["src/index.js"],
            "unstaged_files": [],
            "untracked_files": None
        }

        output = to_yaml(data)

        expected = {
            "action": "status",
            "staged_files": ["src/index.js"]
        }

        self.assertEqual(
            yaml.safe_load(output),
            expected
        )

    def test_yaml_string_escaping(self):
        """Strings containing YAML special characters should survive serialization."""
        data = {
            "files": [
                "styles/[main].css",
                "normal-file.txt"
            ]
        }

        output = to_yaml(data)

        self.assertEqual(
            yaml.safe_load(output),
            data
        )


if __name__ == "__main__":
    unittest.main()