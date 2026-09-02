import re
from pathlib import Path

from django.test import SimpleTestCase


class KeysFileTests(SimpleTestCase):
    keys_path = Path(__file__).resolve().parents[2] / "KEYS"
    assignment_pattern = re.compile(
        r'(?P<name>[A-Za-z_][A-Za-z0-9_]*)="(?P<value>[^"\r\n]*)"'
    )

    def read_assignments(self):
        contents = self.keys_path.read_text(encoding="utf-8")
        assignments = []

        for line_number, line in enumerate(contents.splitlines(), start=1):
            match = self.assignment_pattern.fullmatch(line)
            self.assertIsNotNone(
                match,
                f"KEYS line {line_number} is not a quoted environment assignment",
            )
            assignments.append(match.groupdict())

        return contents, assignments

    def test_keys_file_contains_all_required_assignments(self):
        _, assignments = self.read_assignments()

        self.assertSetEqual(
            {assignment["name"] for assignment in assignments},
            {"secret", "API_KEY"},
        )

    def test_keys_file_values_are_not_empty_or_whitespace(self):
        _, assignments = self.read_assignments()

        for assignment in assignments:
            with self.subTest(name=assignment["name"]):
                self.assertTrue(assignment["value"].strip())

    def test_keys_file_does_not_redeclare_variables(self):
        _, assignments = self.read_assignments()
        names = [assignment["name"] for assignment in assignments]

        self.assertEqual(len(names), len(set(names)))

    def test_keys_file_is_utf8_text_ending_with_a_newline(self):
        contents, _ = self.read_assignments()

        self.assertTrue(contents.endswith("\n"))

    def test_keys_file_is_not_executable(self):
        self.assertEqual(self.keys_path.stat().st_mode & 0o111, 0)
