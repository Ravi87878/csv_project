import re
from pathlib import Path

from django.test import SimpleTestCase


class KeysFileTests(SimpleTestCase):
    keys_path = Path(__file__).resolve().parents[2] / 'KEYS'
    assignment_pattern = re.compile(
        r'^(?P<name>[A-Za-z_][A-Za-z0-9_]*)=(?P<quote>["\'])(?P<value>.+)(?P=quote)$'
    )

    def _configuration_lines(self):
        return [
            line.strip()
            for line in self.keys_path.read_text(encoding='utf-8').splitlines()
            if line.strip() and not line.lstrip().startswith('#')
        ]

    def test_keys_file_defines_required_non_empty_values(self):
        assignments = {}

        for line in self._configuration_lines():
            match = self.assignment_pattern.fullmatch(line)
            if match:
                assignments[match.group('name')] = match.group('value')

        for required_name in ('secret', 'API_KEY'):
            with self.subTest(name=required_name):
                self.assertIn(required_name, assignments)
                self.assertTrue(assignments[required_name])

    def test_keys_file_contains_only_unique_quoted_assignments(self):
        names = []

        for line_number, line in enumerate(self._configuration_lines(), start=1):
            with self.subTest(line_number=line_number):
                match = self.assignment_pattern.fullmatch(line)
                self.assertIsNotNone(
                    match,
                    'KEYS entries must be simple quoted assignments',
                )
                names.append(match.group('name'))

        self.assertEqual(len(names), len(set(names)), 'KEYS contains duplicate names')

    def test_keys_file_is_not_executable(self):
        self.assertEqual(self.keys_path.stat().st_mode & 0o111, 0)
