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

# File purpose: Main script to generate replay sequence from a P2J tree.
# Usage: For Bob to generate replay sequence from the enhanced specification.

import sys
import pickle as pkl

from . import ExecutionTree as exT
from .algorithms import pc


def replay_sequence(tree_binary, cache_size, replay_order_binary):
    with open(tree_binary, 'rb') as tbf:
        p2j_execution_tree = pkl.load(tbf)
    tree = exT.create_tree('P2J', p2j_execution_tree)
    tree.cache_size = cache_size
    pc(tree)
    with open(replay_order_binary, 'wb') as robf:
        pkl.dump((p2j_execution_tree.root, tree), robf)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Usage replay-order-p2j.py pc|prpv1|prpv2|lfu <cache_size> <input tree.bin> <output replay-order.bin>')

    if sys.argv[1] in ['pc']:
        replay_sequence(sys.argv[3], float(sys.argv[2]), sys.argv[4])
    elif sys.argv[1] in ['prpv1', 'prpv2', 'lfu']:
        raise NotImplementedError(f'{sys.argv[1]} Replay Order Not Implemented')
    else:
        print('Usage replay-order.py pc|prpv1|prpv2|lfu <cache_size> <input tree.bin> <output replay-order.bin>')
