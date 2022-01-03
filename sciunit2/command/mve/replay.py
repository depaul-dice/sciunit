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

# File purpose: Main script to re-run an execution using a replay sequence and checkpointing with CRIU.
# Usage: For Bob to use the replay sequence to run the execution.

import os
import sys
import subprocess
import socket
import pickle
import time
import signal
import shutil
import base64
import pickle as pkl
import inspect

import psutil

from .runner_util import *
from . import runner as runner_import


def criu_directory(hash_directory):
    return 'criu_' + base64.b64encode(hash_directory.encode()).decode().replace('/', '_')


def delete_checkpoint(hash_directory):
    directory = criu_directory(hash_directory)
    shutil.rmtree(directory, ignore_errors=True)


def criu_dump(pid, hash_directory, waiter=None):
    delete_checkpoint(hash_directory)
    directory = criu_directory(hash_directory)
    os.mkdir(directory)
    os.system(f'sudo criu dump -t {pid} --shell-job -D {directory}/')
    if waiter is not None:
        waiter.wait()
    while psutil.pid_exists(pid):
        time.sleep(.1)
    time.sleep(.2)


def criu_restore(pid, hash_directory):
    while psutil.pid_exists(pid):
        time.sleep(.1)
    directory = criu_directory(hash_directory)
    # os.system(f'sudo criu restore --shell-job -D {directory}/ &')
    runner = subprocess.Popen(['sudo', 'criu', 'restore', '--shell-job', '-D', f'{directory}/'], start_new_session=True)
    while not psutil.pid_exists(pid):
        time.sleep(.1)
    signal.pause()
    signal.pause()
    return runner


def run_code(server, pid, code):
    while not psutil.pid_exists(pid):
        time.sleep(.1)
    time.sleep(.1)
    while True:
        try:
            os.kill(pid, signal.SIGUSR1)
            break
        except PermissionError:
            pass
    conn, _ = server.accept()
    send_msg(conn, pickle.dumps(code))
    result = pickle.loads(recv_msg(conn))
    conn.close()
    return result


def make_code_map(node, code_map):
    code_map[node.hash] = node.code
    for child in node.children:
        make_code_map(child, code_map)


def replay(replay_order_binary, verbose=False):
    with open(replay_order_binary, 'rb') as robf:
        p2j_execution_tree, tree = pkl.load(robf)
    start = time.time()

    code_map = {}
    make_code_map(p2j_execution_tree, code_map)

    try:
        os.unlink(SOCKET_FILE)
    except FileNotFoundError:
        pass
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_FILE)
    server.listen(1)

    signal.signal(signal.SIGUSR1, lambda *_: None)

    runner = subprocess.Popen(['python', inspect.getsourcefile(runner_import)], start_new_session=True)

    cconn, _ = server.accept()
    runner_pid = pickle.loads(recv_msg(cconn))
    send_msg(cconn, pickle.dumps(os.getpid()))
    cconn.close()
    # print(runner_pid)

    criu_dump(runner_pid, tree.root, runner)
    runner = criu_restore(runner_pid, tree.root)
    # print('First Restore Done')

    if verbose: tree.show(line_type="ascii-em")
    def rec_run(node, cache=tree.cache_size, create=[tree.root]):
        nonlocal runner
        to_checkpoint = any(rc[1] for rc in node.data.recursive_cache[cache])

        for i, (child, to_cache) in enumerate(node.data.recursive_cache[cache]):
            if child is node:
                if i == 0:
                    if verbose: print(f'Running {node.identifier}')
                    out = run_code(server, runner_pid, code_map[node.identifier])
                    if out: print(out)
                    if to_checkpoint:
                        criu_dump(runner_pid, node.identifier, runner)
                        runner = criu_restore(runner_pid, node.identifier)
                else:
                    restore, *run = create
                    criu_dump(runner_pid, 'criu', runner)
                    if verbose: print(f'Restoring {restore.identifier}')
                    runner = criu_restore(runner_pid, restore.identifier)
                    for r in run:
                        if verbose: print(f'Running {r.identifier}')
                        out = run_code(server, runner_pid, code_map[r.identifier])
                        if out: print(out)
            else:
                if to_cache:
                    rec_run(child, cache - node.data.c_size, [node, child])
                    criu_dump(runner_pid, 'criu', runner)
                    if verbose: print(f'Restoring {node.identifier}')
                    runner = criu_restore(runner_pid, node.identifier)
                else:
                    rec_run(child, cache, create + [child])
        
        if to_checkpoint:
            delete_checkpoint(node.identifier)

    rec_run(tree.get_node(tree.root))
    os.system(f'sudo kill -KILL {runner_pid}')
    print(f'Total Time = {time.time() - start}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: replay.py replay-order.bin')
    replay(sys.argv[1])
