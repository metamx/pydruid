# -*- coding: UTF-8 -*-

import pytest

from pydruid.utils import dimensions, filters


class TestDimension:
    def test_dimension(self):
        d = filters.Dimension("dim")
        actual = filters.Filter.build_filter(d == "val")
        expected = {"type": "selector", "dimension": "dim", "value": "val"}
        assert actual == expected

    def test_ne_dimension(self):
        d = filters.Dimension("dim")
        actual = filters.Filter.build_filter(d != "val")
        expected = {
            "field": {"dimension": "dim", "type": "selector", "value": "val"},
            "type": "not",
        }
        assert actual == expected


class TestFilter:
    def test_selector_filter(self):
        actual = filters.Filter.build_filter(
            filters.Filter(dimension="dim", value="val")
        )
        expected = {"type": "selector", "dimension": "dim", "value": "val"}
        assert actual == expected

    def test_selector_filter_extraction_fn(self):
        extraction_fn = dimensions.RegexExtraction("([a-b])")
        f = filters.Filter(
            dimension="dim", value="v", extraction_function=extraction_fn
        )
        actual = filters.Filter.build_filter(f)
        expected = {
            "type": "selector",
            "dimension": "dim",
            "value": "v",
            "extractionFn": {"type": "regex", "expr": "([a-b])"},
        }
        assert actual == expected

    def test_extraction_filter(self):
        extraction_fn = dimensions.PartialExtraction("([a-b])")
        f = filters.Filter(
            type="extraction",
            dimension="dim",
            value="v",
            extraction_function=extraction_fn,
        )
        actual = filters.Filter.build_filter(f)
        expected = {
            "type": "extraction",
            "dimension": "dim",
            "value": "v",
            "extractionFn": {"type": "partial", "expr": "([a-b])"},
        }
        assert actual == expected

    def test_javascript_filter(self):
        actual = filters.Filter.build_filter(
            filters.Filter(
                type="javascript", dimension="dim", function="function(x){return true}"
            )
        )
        expected = {
            "type": "javascript",
            "dimension": "dim",
            "function": "function(x){return true}",
        }
        assert actual == expected

    def test_bound_filter(self):
        actual = filters.Filter.build_filter(
            filters.Bound(
                dimension="dim",
                lower="1",
                lowerStrict=True,
                upper="10",
                upperStrict=True,
                ordering="numeric",
            )
        )
        expected = {
            "type": "bound",
            "dimension": "dim",
            "lower": "1",
            "lowerStrict": True,
            "upper": "10",
            "upperStrict": True,
            "alphaNumeric": False,
            "ordering": "numeric",
        }
        assert actual == expected

    def test_bound_filter_with_extraction_function(self):
        f = filters.Bound(
            dimension="d",
            lower="1",
            upper="3",
            upperStrict=True,
            extraction_function=dimensions.RegexExtraction(".*([0-9]+)"),
        )
        actual = filters.Filter.build_filter(f)
        expected = {
            "type": "bound",
            "dimension": "d",
            "lower": "1",
            "lowerStrict": False,
            "upper": "3",
            "upperStrict": True,
            "ordering": "lexicographic",
            "alphaNumeric": False,
            "extractionFn": {"type": "regex", "expr": ".*([0-9]+)"},
        }
        assert actual == expected

    def test_bound_filter_alphanumeric(self):
        actual = filters.Filter.build_filter(
            filters.Bound(
                dimension="dim",
                lower="1",
                lowerStrict=True,
                upper="10",
                upperStrict=True,
                alphaNumeric=True,
            )
        )
        expected = {
            "type": "bound",
            "dimension": "dim",
            "lower": "1",
            "lowerStrict": True,
            "upper": "10",
            "upperStrict": True,
            "alphaNumeric": True,
            "ordering": "lexicographic",
        }
        assert actual == expected

    def test_bound_filter_lower_not_included(self):
        actual = filters.Filter.build_filter(
            filters.Bound(dimension="dim", upper="10", upperStrict=True)
        )
        expected = {
            "type": "bound",
            "dimension": "dim",
            "lower": None,
            "lowerStrict": False,
            "upper": "10",
            "upperStrict": True,
            "alphaNumeric": False,
            "ordering": "lexicographic",
        }
        assert actual == expected

    def test_spatial_filter_rectangle(self):
        actual = filters.Filter.build_filter(
            filters.Spatial(
                dimension="dim",
                bound_type="rectangle",
                minCoords=[100.0, 100.0],
                maxCoords=[100.1, 100.1],
                radius=10.0,
            )
        )
        expected = {
            "type": "spatial",
            "dimension": "dim",
            "bound": {
                "type": "rectangle",
                "minCoords": [100.0, 100.0],
                "maxCoords": [100.1, 100.1],
            },
        }
        assert actual == expected

    def test_spatial_filter_radius(self):
        actual = filters.Filter.build_filter(
            filters.Spatial(
                dimension="dim",
                bound_type="radius",
                coords=[100.0, 100.0],
                radius=100.0,
            )
        )
        expected = {
            "type": "spatial",
            "dimension": "dim",
            "bound": {"type": "radius", "coords": [100.0, 100.0], "radius": 100.0},
        }
        assert actual == expected

    def test_spatial_filter_polygon(self):
        actual = filters.Filter.build_filter(
            filters.Spatial(
                dimension="dim",
                bound_type="polygon",
                abscissa=[2.0, 3.0, 7.0, 8.0],
                ordinate=[4.0, 9.0, 8.0, 1.0],
            )
        )
        expected = {
            "type": "spatial",
            "dimension": "dim",
            "bound": {
                "type": "polygon",
                "abscissa": [2.0, 3.0, 7.0, 8.0],
                "ordinate": [4.0, 9.0, 8.0, 1.0],
            },
        }
        assert actual == expected

    def test_interval_filter(self):
        actual = filters.Filter.build_filter(
            filters.Interval(
                dimension="dim",
                intervals=["2014-10-01T00:00:00.000Z/2014-10-07T00:00:00.000Z"],
            )
        )
        expected = {
            "type": "interval",
            "dimension": "dim",
            "intervals": ["2014-10-01T00:00:00.000Z/2014-10-07T00:00:00.000Z"],
        }
        assert actual == expected

    def test_interval_with_extraction_function(self):
        f = filters.Interval(
            dimension="dim",
            intervals=["2014-10-01T00:00:00.000Z/2014-10-07T00:00:00.000Z"],
            extraction_function=dimensions.RegexExtraction(".*([0-9]+)"),
        )
        actual = filters.Filter.build_filter(f)
        expected = {
            "type": "interval",
            "dimension": "dim",
            "intervals": ["2014-10-01T00:00:00.000Z/2014-10-07T00:00:00.000Z"],
            "extractionFn": {"type": "regex", "expr": ".*([0-9]+)"},
        }
        assert actual == expected

    def test_and_filter(self):
        f1 = filters.Filter(dimension="dim1", value="val1")
        f2 = filters.Filter(dimension="dim2", value="val2")
        actual = filters.Filter.build_filter(f1 & f2)
        expected = {
            "type": "and",
            "fields": [
                {"type": "selector", "dimension": "dim1", "value": "val1"},
                {"type": "selector", "dimension": "dim2", "value": "val2"},
            ],
        }
        assert actual == expected

    def test_and_filter_multiple(self):
        f1 = filters.Filter(dimension="dim1", value="val1")
        f2 = filters.Filter(dimension="dim2", value="val2")
        f3 = filters.Filter(dimension="dim3", value="val3")
        filter = filters.Filter(type="and", fields=[f1, f2, f3])
        actual = filters.Filter.build_filter(filter)
        expected = {
            "type": "and",
            "fields": [
                {"type": "selector", "dimension": "dim1", "value": "val1"},
                {"type": "selector", "dimension": "dim2", "value": "val2"},
                {"type": "selector", "dimension": "dim3", "value": "val3"},
            ],
        }
        assert actual == expected

    def test_or_filter(self):
        f1 = filters.Filter(dimension="dim1", value="val1")
        f2 = filters.Filter(dimension="dim2", value="val2")
        actual = filters.Filter.build_filter(f1 | f2)
        expected = {
            "type": "or",
            "fields": [
                {"type": "selector", "dimension": "dim1", "value": "val1"},
                {"type": "selector", "dimension": "dim2", "value": "val2"},
            ],
        }
        assert actual == expected

    def test_nested_mix_filter(self):
        f1 = filters.Filter(dimension="dim1", value="val1")
        f2 = filters.Filter(dimension="dim2", value="val2")
        f3 = filters.Filter(dimension="dim3", value="val3")
        f4 = filters.Filter(dimension="dim4", value="val4")
        f5 = filters.Filter(dimension="dim5", value="val5")
        f6 = filters.Filter(dimension="dim6", value="val6")
        f7 = filters.Filter(dimension="dim7", value="val7")
        f8 = filters.Filter(dimension="dim8", value="val8")
        actual = filters.Filter.build_filter(
            f1 & ~f2 & f3 & (f4 | ~f5 | f6 | (f7 & ~f8))
        )
        expected = {
            "fields": [
                {"dimension": "dim1", "type": "selector", "value": "val1"},
                {
                    "field": {"dimension": "dim2", "type": "selector", "value": "val2"},
                    "type": "not",
                },
                {"dimension": "dim3", "type": "selector", "value": "val3"},
                {
                    "fields": [
                        {"dimension": "dim4", "type": "selector", "value": "val4"},
                        {
                            "field": {
                                "dimension": "dim5",
                                "type": "selector",
                                "value": "val5",
                            },
                            "type": "not",
                        },
                        {"dimension": "dim6", "type": "selector", "value": "val6"},
                        {
                            "fields": [
                                {
                                    "dimension": "dim7",
                                    "type": "selector",
                                    "value": "val7",
                                },
                                {
                                    "field": {
                                        "dimension": "dim8",
                                        "type": "selector",
                                        "value": "val8",
                                    },
                                    "type": "not",
                                },
                            ],
                            "type": "and",
                        },
                    ],
                    "type": "or",
                },
            ],
            "type": "and",
        }
        assert actual == expected

    def test_or_filter_multiple(self):
        f1 = filters.Filter(dimension="dim1", value="val1")
        f2 = filters.Filter(dimension="dim2", value="val2")
        f3 = filters.Filter(dimension="dim3", value="val3")
        filter = filters.Filter(type="or", fields=[f1, f2, f3])
        actual = filters.Filter.build_filter(filter)
        expected = {
            "type": "or",
            "fields": [
                {"type": "selector", "dimension": "dim1", "value": "val1"},
                {"type": "selector", "dimension": "dim2", "value": "val2"},
                {"type": "selector", "dimension": "dim3", "value": "val3"},
            ],
        }
        assert actual == expected

    def test_not_filter(self):
        f = ~filters.Filter(dimension="dim", value="val")
        actual = filters.Filter.build_filter(f)
        # Call `build_filter` twice to make sure it does not
        # change the passed filter object argument `f`.
        actual = filters.Filter.build_filter(f)
        expected = {
            "type": "not",
            "field": {"type": "selector", "dimension": "dim", "value": "val"},
        }
        assert actual == expected

    def test_nested_not_or_filter(self):
        f1 = filters.Filter(dimension="dim1", value="val1")
        f2 = filters.Filter(dimension="dim2", value="val2")
        actual = filters.Filter.build_filter(~(f1 | f2))
        expected = {
            "type": "not",
            "field": {
                "type": "or",
                "fields": [
                    {"type": "selector", "dimension": "dim1", "value": "val1"},
                    {"type": "selector", "dimension": "dim2", "value": "val2"},
                ],
            },
        }
        assert actual == expected

    def test_in_filter(self):
        actual = filters.Filter.build_filter(
            filters.Filter(type="in", dimension="dim", values=["val1", "val2", "val3"])
        )
        expected = {
            "type": "in",
            "dimension": "dim",
            "values": ["val1", "val2", "val3"],
        }
        assert actual == expected

    def test_not_in_filter(self):
        actual = filters.Filter.build_filter(
            ~filters.Filter(type="in", dimension="dim", values=["val1", "val2", "val3"])
        )
        expected = {
            "type": "not",
            "field": {
                "type": "in",
                "dimension": "dim",
                "values": ["val1", "val2", "val3"],
            },
        }
        assert actual == expected

    def test_invalid_filter(self):
        with pytest.raises(NotImplementedError):
            filters.Filter(type="invalid", dimension="dim", value="val")

    def test_columnComparison_filter(self):
        actual = filters.Filter.build_filter(
            filters.Filter(
                type="columnComparison",
                dimensions=["dim1", dimensions.DimensionSpec("dim2", "dim2")],
            )
        )
        expected = {
            "type": "columnComparison",
            "dimensions": [
                "dim1",
                {"type": "default", "dimension": "dim2", "outputName": "dim2"},
            ],
        }
        assert actual == expected

    def test_search_filter(self):
        # Without caseSensitive param - default:false
        actual = filters.Filter.build_filter(
            filters.Filter(type="search", dimension="dim", value="val")
        )
        expected = {
            "type": "search",
            "dimension": "dim",
            "query": {"type": "contains", "caseSensitive": "false", "value": "val"},
        }
        assert actual == expected

        # With caseSensitive param
        actual = filters.Filter.build_filter(
            filters.Filter(
                type="search", dimension="dim", value="val", caseSensitive="true"
            )
        )
        expected = {
            "type": "search",
            "dimension": "dim",
            "query": {"type": "contains", "caseSensitive": "true", "value": "val"},
        }
        assert actual == expected

    def test_search_filter_with_extraction_function(self):
        extraction_fn = dimensions.RegexExtraction("([a-b])")
        actual = filters.Filter.build_filter(
            filters.Filter(
                type="search",
                dimension="dim",
                value="val",
                extraction_function=extraction_fn,
            )
        )
        expected = {
            "type": "search",
            "dimension": "dim",
            "query": {"type": "contains", "caseSensitive": "false", "value": "val"},
            "extractionFn": {"type": "regex", "expr": "([a-b])"},
        }
        assert actual == expected

    def test_like_filter(self):
        actual = filters.Filter.build_filter(
            filters.Filter(type="like", dimension="dim", pattern="%val%")
        )
        expected = {"type": "like", "dimension": "dim", "pattern": "%val%"}
        assert actual == expected

    def test_like_filter_with_extraction_function(self):
        extraction_fn = dimensions.RegexExtraction("([a-b])")
        actual = filters.Filter.build_filter(
            filters.Filter(
                type="like",
                dimension="dim",
                pattern="%val%",
                extraction_function=extraction_fn,
            )
        )
        expected = {
            "type": "like",
            "dimension": "dim",
            "pattern": "%val%",
            "extractionFn": {"type": "regex", "expr": "([a-b])"},
        }
        assert actual == expected
