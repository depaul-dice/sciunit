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

# File purpose: Miscellaneous utility functions

from functools import singledispatch
from itertools import islice


def create_registerer():
    @singledispatch
    def call(key, *args, **kwargs):
        """Use this function to call a registered function based on key"""
        return call.map[key](*args, **kwargs)

    @call.register
    def _(key: int, *args, **kwargs):
        """Use index rather than the key"""
        assert 1 <= key <= len(call.map)
        return next(islice(call.map.values(),
                           key - 1,
                           len(call.map)))(*args, **kwargs)

    call.map = {}

    def register_callee(key):
        """Use this decorator to register a callee"""
        assert not isinstance(key, int)

        def register(callee):
            call.map[key] = callee
            call.__doc__ += f'\n{len(call.map)}. {key}'
            return callee

        if callable(key):
            creator, key = key, key.__name__
            return register(creator)
        else:
            return register

    return call, register_callee


def dfs_cost(ex_tree, node=None, force_cost=None):
    """Compute cost of computing entire tree recursively"""
    if node is None:
        ex_tree.total_r_cost = 0
        node = ex_tree.get_node(ex_tree.root)
    for child in ex_tree.children(node.identifier):
        dfs_cost(ex_tree, child, force_cost)
    if node.is_leaf():
        node.data.y = 1
    else:
        # compute y value for all children
        node.data.y = 0  # reinitialize for repeated runs
        for child in ex_tree.children(node.identifier):
            node.data.y += 1 + (child.data.y - 1) * (1 - child.data.x_in_cache)

    if not force_cost:
        ex_tree.total_r_cost += node.data.r_cost * (1 + (node.data.y - 1) * (1 - node.data.x_in_cache))
    else:
        ex_tree.total_r_cost += force_cost * (1 + (node.data.y - 1) * (1 - node.data.x_in_cache))
    return ex_tree.total_r_cost


def non_dfs_cost(ex_tree):
    """Compute the cost for a non-DFS solution"""
    return sum(node.data.r_cost * sum(node.data.p_computed) for node in ex_tree.all_nodes_itr())


def cost(ex_tree):
    """Auto compute for both DFS and non-DFS solution"""
    if ex_tree.get_node(ex_tree.root).data.p_computed:
        return non_dfs_cost(ex_tree)
    elif ex_tree.get_node(ex_tree.root).data.recursive_cache:
        return ex_tree.total_cost
    else:
        return dfs_cost(ex_tree)


def _min_max_depth(ex_tree, node=None):
    if node is None:
        node = ex_tree.root
    depths = []
    for child in ex_tree.children(node):
        depths.extend(_min_max_depth(ex_tree, child.identifier))
    if not depths:
        return 1, 1
    return 1 + min(depths), 1 + max(depths)


def print_info(ex_tree, name=''):
    if name:
        print(name)
    print('Leaves', len(ex_tree.leaves(ex_tree.root)))
    print('Total Cost', cost(ex_tree))
    print('Min Cost', min(node.data.r_cost for node in ex_tree.all_nodes()
                          if node.data.r_cost != 0))
    print('Max Cost', max(node.data.r_cost for node in ex_tree.all_nodes()))
    print('Total Storage', sum(node.data.c_size for node in ex_tree.all_nodes()
                               if node.data.c_size != float('inf')))
    print('Min Storage', min(node.data.c_size for node in ex_tree.all_nodes()))
    print('Max Storage', max(node.data.c_size for node in ex_tree.all_nodes()
                             if node.data.c_size != float('inf')))
    print('Min/Max Depths', *_min_max_depth(ex_tree))


def paths_to_leaves(ex_tree, node_path=None):
    if node_path is None:
        node, path = ex_tree.get_node(ex_tree.root), []
    else:
        node, path = node_path
    path.append(node)
    if node.is_leaf():
        yield path.copy()
    else:
        for child in ex_tree.children(node.identifier):
            yield from paths_to_leaves(ex_tree, node_path=(child, path))
    assert path.pop() == node


def checkpoints_restores(ex_tree):
    def recurse(node, cache):
        cr = 0
        for child, p_in_c in node.data.recursive_cache[cache]:
            if p_in_c:
                cr += 1
            if child is not node:
                cr += recurse(child, cache - (node.data.c_size
                                              if p_in_c else 0))
        return cr

    return recurse(ex_tree.get_node(ex_tree.root), ex_tree.cache_size)

