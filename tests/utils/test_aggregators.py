# -*- coding: UTF-8 -*-

from copy import deepcopy
from operator import itemgetter

from pydruid.utils import aggregators, filters


class TestAggregators:
    def test_aggregators(self):
        aggs = [
            ("longsum", "longSum"),
            ("longmin", "longMin"),
            ("longmax", "longMax"),
            ("doublesum", "doubleSum"),
            ("doublemin", "doubleMin"),
            ("doublemax", "doubleMax"),
            ("doublemean", "doubleMean"),
            ("count", "count"),
            ("hyperunique", "hyperUnique"),
            ("stringfirst", "stringFirst"),
            ("stringlast", "stringLast"),
        ]
        aggs_funcs = [
            (getattr(aggregators, agg_name), agg_type) for agg_name, agg_type in aggs
        ]
        for f, agg_type in aggs_funcs:
            assert f("metric") == {"type": agg_type, "fieldName": "metric"}

    def test_filtered_aggregator(self):
        filter_ = filters.Filter(dimension="dim", value="val")
        aggs = [
            aggregators.count("metric1"),
            aggregators.longsum("metric2"),
            aggregators.doublesum("metric3"),
            aggregators.doublemin("metric4"),
            aggregators.doublemax("metric5"),
            aggregators.doublemean("metric6"),
            aggregators.hyperunique("metric7"),
            aggregators.cardinality("dim1"),
            aggregators.cardinality(["dim1", "dim2"], by_row=True),
            aggregators.thetasketch("dim1"),
            aggregators.thetasketch("metric8"),
            aggregators.thetasketch("metric9", isinputthetasketch=True, size=8192),
        ]
        for agg in aggs:
            expected = {
                "type": "filtered",
                "filter": {"type": "selector", "dimension": "dim", "value": "val"},
                "aggregator": agg,
            }
            actual = aggregators.filtered(filter_, agg)
            assert actual == expected

    def test_nested_filtered_aggregator(self):
        filter1 = filters.Filter(dimension="dim1", value="val")
        filter2 = filters.Filter(dimension="dim2", value="val")
        agg = aggregators.filtered(
            filter1, aggregators.filtered(filter2, aggregators.count("metric1"))
        )
        actual = aggregators.build_aggregators({"agg_name": agg})
        # the innermost aggregation must have 'agg_name'
        expected = [
            {
                "type": "filtered",
                "aggregator": {
                    "type": "filtered",
                    "aggregator": {
                        "fieldName": "metric1",
                        "type": "count",
                        "name": "agg_name",
                    },
                    "filter": {"dimension": "dim2", "value": "val", "type": "selector"},
                },
                "filter": {"dimension": "dim1", "value": "val", "type": "selector"},
            }
        ]
        assert expected == actual

    def test_build_aggregators(self):
        agg_input = {
            "agg1": aggregators.count("metric1"),
            "agg2": aggregators.longsum("metric2"),
            "agg3": aggregators.doublesum("metric3"),
            "agg4": aggregators.doublemin("metric4"),
            "agg5": aggregators.doublemax("metric5"),
            "agg6": aggregators.doublemean("metric6"),
            "agg7": aggregators.hyperunique("metric7"),
            "agg8": aggregators.cardinality("dim1"),
            "agg9": aggregators.cardinality(["dim1", "dim2"], by_row=True),
            "agg10": aggregators.thetasketch("dim1"),
            "agg11": aggregators.thetasketch("metric8"),
            "agg12": aggregators.thetasketch(
                "metric9", isinputthetasketch=True, size=8192
            ),
        }
        built_agg = aggregators.build_aggregators(agg_input)
        expected = [
            {"name": "agg1", "type": "count", "fieldName": "metric1"},
            {"name": "agg2", "type": "longSum", "fieldName": "metric2"},
            {"name": "agg3", "type": "doubleSum", "fieldName": "metric3"},
            {"name": "agg4", "type": "doubleMin", "fieldName": "metric4"},
            {"name": "agg5", "type": "doubleMax", "fieldName": "metric5"},
            {"name": "agg6", "type": "doubleMean", "fieldName": "metric6"},
            {"name": "agg7", "type": "hyperUnique", "fieldName": "metric7"},
            {
                "name": "agg8",
                "type": "cardinality",
                "fieldNames": ["dim1"],
                "byRow": False,
            },
            {
                "name": "agg9",
                "type": "cardinality",
                "fieldNames": ["dim1", "dim2"],
                "byRow": True,
            },
            {
                "name": "agg10",
                "type": "thetaSketch",
                "fieldName": "dim1",
                "isInputThetaSketch": False,
                "size": 16384,
            },
            {
                "name": "agg11",
                "type": "thetaSketch",
                "fieldName": "metric8",
                "isInputThetaSketch": False,
                "size": 16384,
            },
            {
                "name": "agg12",
                "type": "thetaSketch",
                "fieldName": "metric9",
                "isInputThetaSketch": True,
                "size": 8192,
            },
        ]
        assert sorted(built_agg, key=itemgetter("name")) == sorted(
            expected, key=itemgetter("name")
        )

    def test_build_filtered_aggregator(self):
        filter_ = filters.Filter(dimension="dim", value="val")
        agg_input = {
            "agg1": aggregators.filtered(filter_, aggregators.count("metric1")),
            "agg2": aggregators.filtered(filter_, aggregators.longsum("metric2")),
            "agg3": aggregators.filtered(filter_, aggregators.doublesum("metric3")),
            "agg4": aggregators.filtered(filter_, aggregators.doublemin("metric4")),
            "agg5": aggregators.filtered(filter_, aggregators.doublemax("metric5")),
            "agg5": aggregators.filtered(filter_, aggregators.doublemean("metric6")),
            "agg7": aggregators.filtered(filter_, aggregators.hyperunique("metric7")),
            "agg8": aggregators.filtered(filter_, aggregators.cardinality("dim1")),
            "agg9": aggregators.filtered(
                filter_, aggregators.cardinality(["dim1", "dim2"], by_row=True)
            ),
            "agg10": aggregators.filtered(filter_, aggregators.thetasketch("dim1")),
            "agg11": aggregators.filtered(filter_, aggregators.thetasketch("metric7")),
            "agg12": aggregators.filtered(
                filter_,
                aggregators.thetasketch("metric8", isinputthetasketch=True, size=8192),
            ),
        }
        base = {
            "type": "filtered",
            "filter": {"type": "selector", "dimension": "dim", "value": "val"},
        }

        aggs = [
            {"name": "agg1", "type": "count", "fieldName": "metric1"},
            {"name": "agg2", "type": "longSum", "fieldName": "metric2"},
            {"name": "agg3", "type": "doubleSum", "fieldName": "metric3"},
            {"name": "agg4", "type": "doubleMin", "fieldName": "metric4"},
            {"name": "agg5", "type": "doubleMax", "fieldName": "metric5"},
            {"name": "agg6", "type": "doubleMean", "fieldName": "metric6"},
            {"name": "agg7", "type": "hyperUnique", "fieldName": "metric7"},
            {
                "name": "agg8",
                "type": "cardinality",
                "fieldNames": ["dim1"],
                "byRow": False,
            },
            {
                "name": "agg9",
                "type": "cardinality",
                "fieldNames": ["dim1", "dim2"],
                "byRow": True,
            },
            {
                "name": "agg10",
                "type": "thetaSketch",
                "fieldName": "dim1",
                "isInputThetaSketch": False,
                "size": 16384,
            },
            {
                "name": "agg11",
                "type": "thetaSketch",
                "fieldName": "metric7",
                "isInputThetaSketch": False,
                "size": 16384,
            },
            {
                "name": "agg12",
                "type": "thetaSketch",
                "fieldName": "metric8",
                "isInputThetaSketch": True,
                "size": 8192,
            },
        ]
        expected = []
        for agg in aggs:
            exp = deepcopy(base)
            exp.update({"aggregator": agg})
            expected.append(exp)

        built_agg = aggregators.build_aggregators(agg_input)
        expected = sorted(
            built_agg, key=lambda k: itemgetter("name")(itemgetter("aggregator")(k))
        )
        actual = sorted(
            expected, key=lambda k: itemgetter("name")(itemgetter("aggregator")(k))
        )
        assert expected == actual
