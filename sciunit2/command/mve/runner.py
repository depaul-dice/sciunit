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

# File purpose: Helper script that gets run in a separate process to get checkpointed/restored by CRIU/

import os
import socket
import pickle
import signal
import time
import code
import io
import sys
import struct


SOCKET_FILE = 'runner.socket'


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


class CodeKernelResult:
    def __init__(self, error_before_exec=None, out=''):
        self.error_before_exec = error_before_exec
        self.out = out

class CodeKernel:
    def __init__(self):
        self.locals = {}
        self.interpreter = code.InteractiveInterpreter(locals=self.locals)
    def run_cell(self, code_in):
        old_stdout, old_stderr = sys.stdout, sys.stderr
        out = io.StringIO()
        sys.stdout = sys.stderr = out
        try:
            code_obj = code.compile_command(code_in, symbol='exec')
            code_in_except = None if code_obj else Exception()
        except Exception as e:
            code_obj = None
            code_in_except = e
        if code_obj: self.interpreter.runcode(code_obj)
        result = CodeKernelResult(code_in_except, out.getvalue())
        sys.stdout, sys.stderr = old_stdout, old_stderr
        return result


kernel = CodeKernel()


def handle_usr1(*_):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_FILE)
    code = pickle.loads(recv_msg(client))

    result = kernel.run_cell(code)
    send_msg(client, pickle.dumps(result.out))
    client.close()


def setup_signal():
    signal.signal(signal.SIGUSR1, handle_usr1)

    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_FILE)
    send_msg(client, pickle.dumps(os.getpid()))
    parent_pid = pickle.loads(recv_msg(client))
    client.close()

    while True:
        time.sleep(1)
        os.kill(parent_pid, signal.SIGUSR1)


if __name__ == '__main__':
    setup_signal()
