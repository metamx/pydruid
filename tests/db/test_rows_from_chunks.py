# -*- coding: utf-8 -*-

import unittest

from pydruid.db.api import rows_from_chunks


class RowsFromChunksTestSuite(unittest.TestCase):
    def test_rows_from_chunks_empty(self):
        chunks = []
        expected = []
        result = list(rows_from_chunks(chunks))
        self.assertEqual(result, expected)

    def test_rows_from_chunks_single_chunk(self):
        chunks = ['[{"name": "alice"}, {"name": "bob"}, {"name": "charlie"}]']
        expected = [{"name": "alice"}, {"name": "bob"}, {"name": "charlie"}]
        result = list(rows_from_chunks(chunks))
        self.assertEqual(result, expected)

    def test_rows_from_chunks_multiple_chunks(self):
        chunks = ['[{"name": "alice"}, {"name": "b', 'ob"}, {"name": "charlie"}]']
        expected = [{"name": "alice"}, {"name": "bob"}, {"name": "charlie"}]
        result = list(rows_from_chunks(chunks))
        self.assertEqual(result, expected)

    def test_rows_from_chunks_bracket_in_string(self):
        chunks = ['[{"name": "ali{ce"}, {"name": "bob"}]']
        expected = [{"name": "ali{ce"}, {"name": "bob"}]
        result = list(rows_from_chunks(chunks))
        self.assertEqual(result, expected)

    def test_rows_from_chunks_quote_in_string(self):
        chunks = [r'[{"name": "ali\"ce"}, {"name": "bob"}]']
        expected = [{"name": 'ali"ce'}, {"name": "bob"}]
        result = list(rows_from_chunks(chunks))
        self.assertEqual(result, expected)

    def test_rows_from_chunks_string_ending_with_backslash(self):
        chunks = [r'[{"name": "\\"}]']
        expected = [{"name": "\\"}]
        result = list(rows_from_chunks(chunks))
        self.assertEqual(result, expected)

    def test_rows_from_chunks_multiple_rows_ending_with_backslashes(self):
        chunks = [r'[{"name": "alice"}, {"name": "bob\\"}, {"name": "charlie\\"}]']
        expected = [{"name": "alice"}, {"name": "bob\\"}, {"name": "charlie\\"}]
        result = list(rows_from_chunks(chunks))
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
