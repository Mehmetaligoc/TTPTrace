import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ttptrace.manifest import ManifestError, load_manifest, validate_manifest  # noqa: E402


class ManifestValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.attack_path = ROOT / "examples" / "attack_manifest.example.json"
        cls.benign_path = ROOT / "examples" / "benign_manifest.example.json"
        cls.attack = json.loads(cls.attack_path.read_text(encoding="utf-8"))

    def test_example_manifests_are_valid(self):
        self.assertEqual(load_manifest(self.attack_path)["session_type"], "attack")
        self.assertEqual(load_manifest(self.benign_path)["session_type"], "benign")

    def test_attack_requires_supported_technique(self):
        data = copy.deepcopy(self.attack)
        data["technique_id"] = "T0000"
        with self.assertRaisesRegex(ManifestError, "unsupported technique_id"):
            validate_manifest(data)

    def test_technique_name_must_match_id(self):
        data = copy.deepcopy(self.attack)
        data["technique_name"] = "Wrong Name"
        with self.assertRaisesRegex(ManifestError, "technique_name"):
            validate_manifest(data)

    def test_authorization_and_isolation_are_mandatory(self):
        data = copy.deepcopy(self.attack)
        data["authorization"]["network_isolated"] = False
        with self.assertRaisesRegex(ManifestError, "network_isolated"):
            validate_manifest(data)

    def test_timestamps_require_timezone_and_order(self):
        data = copy.deepcopy(self.attack)
        data["window"]["ended_at"] = data["window"]["started_at"]
        with self.assertRaisesRegex(ManifestError, "later"):
            validate_manifest(data)

        data = copy.deepcopy(self.attack)
        data["window"]["started_at"] = "2026-09-27T10:00:00"
        with self.assertRaisesRegex(ManifestError, "timezone"):
            validate_manifest(data)

    def test_artifact_path_cannot_escape_project(self):
        data = copy.deepcopy(self.attack)
        data["artifacts"]["event_log"] = "../outside/events.jsonl"
        with self.assertRaisesRegex(ManifestError, "safe relative path"):
            validate_manifest(data)

    def test_benign_session_cannot_have_attack_label(self):
        data = copy.deepcopy(self.attack)
        data["session_type"] = "benign"
        with self.assertRaisesRegex(ManifestError, "must set technique_id"):
            validate_manifest(data)


if __name__ == "__main__":
    unittest.main()

