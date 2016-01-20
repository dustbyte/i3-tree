# -*- coding: utf-8 -*-

import json

import pytest

from i3_tree import i3Tree, i3Node

FIXTURE_PATH="tests/fixtures/i3_tree.json"

NODE_FIELDS = [
    "border",
    "current_border_width",
    "deco_rect",
    "floating",
    "floating_nodes",
    "focus",
    "focused",
    "fullscreen_mode",
    "geometry",
    "id",
    "last_split_layout",
    "layout",
    "name",
    "nodes",
    "orientation",
    "percent",
    "rect",
    "scratchpad_state",
    "swallows",
    "type",
    "urgent",
    "window",
    "window_rect",
    "workspace_layout",
]


@pytest.fixture
def json_tree():
    with open(FIXTURE_PATH, "r") as handle:
        return json.load(handle)


@pytest.fixture
def tree(json_tree):
    return i3Tree(json_tree)


def test_tree_created(json_tree):
    tree = i3Tree(json_tree)
    assert tree.raw_tree
    assert tree.root
    assert tree.root.children
    assert tree.root.children_dict
    assert tree.root.has_focus
    assert tree.root.focused_child


def test_node_attribute(tree):
    """
    Note: window_properties is not necesarily present in a node
    """
    for field in NODE_FIELDS:
        assert hasattr(tree.root, field)


def test_node_keys(tree):
    """
    Note: window_properties is not necesarily present in a node
    """
    for field in NODE_FIELDS:
        _ = tree.root[field]


def test_tree_order(tree):
    root = tree.root
    assert root.type == "root"
    assert root.name == "root"

    assert root.children[0].type == "output"
    assert root.children[0].name == "__i3"

    assert root.children[1].type == "output"
    assert root.children[1].name == "eDP1"

    assert root.children[2].type == "output"
    assert root.children[2].name == "HDMI1"


def test_node_repr(tree):
    expected_value = '<21696960, "root">'
    assert str(tree.root) == expected_value
    assert unicode(tree.root) == expected_value
    assert repr(tree.root) == expected_value


def test_node_filter_conditions(tree):
    i3_output = tree.root.filter(name="__i3")[0]

    assert i3_output.type == "output"


def test_node_filter_no_criteria(tree):
    assert tree.root.filter()[0] == tree.root


def test_node_filter_function(tree):

    def search_func(node):
        return node.type == "output" and node.name != "__i3"

    nodes = tree.root.filter(search_func)
    names = [node.name for node in nodes]

    assert names == ["eDP1", "HDMI1"]


def test_tree_focused(tree):
    assert tree.focused.name == "xterm"
