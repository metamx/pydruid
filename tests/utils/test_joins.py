# -*- coding: UTF-8 -*-
"""
Tests the pydruid.utils.joins module
"""

from pydruid.utils import joins


class TestJoin:
    """ Test cases the pydruid.util.join module """

    def test_join(self):
        join = joins.Join("some", "other", "other_", "a = other_b", join_type="INNER")
        actual = joins.Join.build_join(join)
        expected = {
            "type": "join",
            "joinType": "INNER",
            "condition": "a = other_b",
            "left": "some",
            "right": "other",
            "rightPrefix": "other_",
        }
        assert actual == expected

    def test_inner_join(self):
        """ Tests InnerJoin """
        join = joins.InnerJoin("some", "other", "other_", "a = other_b")
        actual = joins.Join.build_join(join)
        expected = {
            "type": "join",
            "joinType": "INNER",
            "condition": "a = other_b",
            "left": "some",
            "right": "other",
            "rightPrefix": "other_",
        }
        assert actual == expected

    def test_left_join(self):
        """ Tests LeftJoin """
        join = joins.LeftJoin("some", "other", "other_", "a = other_b")
        actual = joins.Join.build_join(join)
        expected = {
            "type": "join",
            "joinType": "LEFT",
            "condition": "a = other_b",
            "left": "some",
            "right": "other",
            "rightPrefix": "other_",
        }
        assert actual == expected

    def test_cross_join(self):
        """ Tests CrossJoin """
        join = joins.CrossJoin("some", "other", "other_")
        actual = joins.Join.build_join(join)
        expected = {
            "type": "join",
            "joinType": "INNER",  # Converts to inner join with condition 1 = 1
            "condition": "1 = 1",
            "left": "some",
            "right": "other",
            "rightPrefix": "other_",
        }
        assert actual == expected
