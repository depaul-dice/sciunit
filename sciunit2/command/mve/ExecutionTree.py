# CHEX - Multiversion Replay with Ordered Checkpoints
# Copyright (c) 2020 DePaul University
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------
#
# Author: Naga Nithin Manne <nithinmanne@gmail.com>

# File purpose: Definition of the Execution Tree data structure and helper function to generate trees.
# Usage: For Bob to create an execution tree from the enhanced specification.

import sys
import random
import uuid
from importlib import import_module

from treelib import Tree

from .util import create_registerer


ENABLE_MAX_HINT = True


class NodeData:

    def __init__(self, r_cost, c_size):
        self.r_cost = r_cost  # corresponds to r in equation
        self.c_size = c_size  # corresponds to c in equation
        self.x_in_cache = False  # corresponds to x in equation
        self.p_computed = []  # corresponds to p in equation
        self.recursive_cache = {}

    def reset(self):
        self.x_in_cache = False
        self.p_computed = []
        self.recursive_cache = {}

    def __sizeof__(self):
        return sum(sys.getsizeof(self.recursive_cache[cache])
                   for cache in self.recursive_cache)


class ExecutionTree(Tree):

    def reset(self):
        for node in self.all_nodes_itr():
            node.data.reset()

    def __sizeof__(self):
        return sum(sys.getsizeof(node.data)
                   for node in self.all_nodes_itr())


create_tree, register_tree_creator = create_registerer()


def fixed_node_factory(_):
    """Create a Node of fixed cost and size"""
    r_cost, c_size = 1, 1
    return NodeData(r_cost, c_size)


def rand_node_factory(height):
    """Create a Node of random cost and size based on height"""
    height = max(1, height)
    r_cost_lim = 10 * height
    c_size_lim = 10 // height
    r_cost = random.randint(max(1, r_cost_lim - 10), r_cost_lim + 10)
    c_size = random.randint(max(1, c_size_lim - 10), c_size_lim + 10)
    return NodeData(r_cost, c_size)


@register_tree_creator('FIXED')
def fixed_tree_creator(node_factory=fixed_node_factory):
    """Create A Fixed Tree"""
    tree = ExecutionTree()
    tree.create_node("A", "a", data=node_factory(0))  # root node
    tree.create_node("B", "b", parent="a", data=node_factory(1))
    tree.create_node("C", "c", parent="b", data=node_factory(2))
    tree.create_node("D", "d", parent="b", data=node_factory(2))
    tree.create_node("E", "e", parent="d", data=node_factory(3))
    tree.create_node("F", "f", parent="d", data=node_factory(3))
    tree.create_node("G", "g", parent="f", data=node_factory(4))
    tree.create_node("H", "h", parent="f", data=node_factory(4))
    tree.create_node("I", "i", parent="f", data=node_factory(4))
    tree.create_node("J", "j", parent="h", data=node_factory(5))
    tree.create_node("K", "k", parent="j", data=node_factory(6))
    tree.create_node("L", "l", parent="k", data=node_factory(7))
    tree.create_node("M", "m", parent="j", data=node_factory(6))
    tree.create_node("N", "n", parent="i", data=node_factory(5))
    tree.create_node("O", "o", parent="n", data=node_factory(6))
    return tree


def _branch_tree_creator_with_hint(k, height, max_nodes, max_leaves, node_factory):
    tree = ExecutionTree()
    tree.create_node("N0", "n0", data=node_factory(0))
    for i in range(1, (k ** (height + 1) - 1) // (k - 1)):
        if random.choice([True, False]) and tree.contains(f'n{(i - 1) // k}'):
            tree.create_node(f'N{i}', f'n{i}', parent=f'n{(i - 1) // k}',
                             data=node_factory(tree.depth(f'n{(i - 1) // k}') + 1))
        if ENABLE_MAX_HINT:
            if max_nodes and len(tree) == max_nodes: return tree
            if max_leaves and len(tree.leaves()) == max_leaves: return tree
    return tree


@register_tree_creator('BRANCH')
def branch_tree_creator(k, height, node_factory=rand_node_factory):
    """Create a random k-ary with the given k and height"""
    return _branch_tree_creator_with_hint(k, height, None, None, node_factory)


@register_tree_creator('KARY')
def kary_tree_creator(k, height, node_factory=fixed_node_factory):
    """Create a perfect k-ary tree with the given k and height"""
    tree = ExecutionTree()
    tree.create_node("N0", "n0", data=node_factory(0))
    for i in range(1, (k ** (height + 1) - 1) // (k - 1)):
        tree.create_node(f'N{i}', f'n{i}', parent=f'n{(i - 1) // k}',
                         data=node_factory(tree.depth(f'n{(i - 1) // k}') + 1))
    return tree


@register_tree_creator('SIZE')
def kary_tree_creator(nodes, k, height, node_factory=fixed_node_factory):
    """Create a k-ary tree with the given size, max k and height"""
    assert nodes <= (k ** (height + 1) - 1) // (k - 1)
    while True:
        tree = _branch_tree_creator_with_hint(k, height, nodes, None, node_factory)
        if tree.size() == nodes: return tree


@register_tree_creator('COUNT')
def kary_tree_creator(leaves, k, height, node_factory=fixed_node_factory):
    """Create a k-ary tree with the given leaves, max k and height"""
    assert leaves <= k ** height
    while True:
        tree = _branch_tree_creator_with_hint(k, height, None, leaves, node_factory)
        if len(tree.leaves()) == leaves: return tree


@register_tree_creator('SCIUNIT')
def sciunit_tree_creator(tree_binary, sciunit_tree_module_path='sciunit_tree'):
    """Create a tree using the real world sciunit tree"""
    sciunit_tree = import_module(sciunit_tree_module_path)
    sciunit_execution_tree, _ = sciunit_tree.tree_load(tree_binary)

    tree = ExecutionTree()

    def recursive_fill(node, parent=None):
        tree.create_node(node.hash, node.hash, parent=parent.hash if parent else None,
                         data=NodeData(node.time, node.size))
        for child in node.children:
            recursive_fill(node.children[child], node)

    sciunit_execution_tree.time = 0
    sciunit_execution_tree.size = float('inf')
    recursive_fill(sciunit_execution_tree)
    return tree

@register_tree_creator('P2J')
def sciunit_tree_creator(p2j_execution_tree):
    """Create a tree using the real world Python2Jupyter repo tree"""
    tree = ExecutionTree()

    count = 0
    def recursive_fill(node, parent=None):
        nonlocal count
        node.hash = f'n{count}'
        count += 1
        tree.create_node(node.hash, node.hash, parent=parent.hash if parent else None,
                         data=NodeData(node.c, node.s))
        for child in node.children:
            recursive_fill(child, node)

    recursive_fill(p2j_execution_tree.root)
    return tree
