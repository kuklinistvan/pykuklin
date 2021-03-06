
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import os
from typing import List

import subprocess
import sys
from multiprocessing import Process

@contextmanager
def working_directory(path: Path) -> None:
    prev_dir = os.getcwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(prev_dir)


def shell(cmd: List[str]) -> None:
    print("[shell] " + list_of_shell_args_to_str(cmd))
    assert 0 == subprocess.call(cmd)


def list_of_shell_args_to_str(cmd: List[str]) -> str:
    """
    Converts ['echo', 'Hello world'] to 'echo "Hello world"'
    """

    args_with_apostroves_where_necessary = []

    for e in cmd:
        if e.find(' ') == -1:
            args_with_apostroves_where_necessary.append(e)
        else:
            args_with_apostroves_where_necessary.append('"' + e + '"')

    return " ".join(args_with_apostroves_where_necessary)



class RemoteShell:
    def __init__(self):
        self._connection = RemoteShell.Connection(self)

    def _initialize(self):
        raise NotImplementedError()

    def _teardown(self):
        raise NotImplementedError()

    def _writeCmd(self, cmd: List[str]):
        raise NotImplementedError()

    class Connection:
        def __init__(self, remoteShell: RemoteShell) -> None:
            self.remoteShell = remoteShell

        def writeCmd(self, cmd: List[str]):
            self.remoteShell._writeCmd(cmd)

    @contextmanager
    def env(self) -> RemoteShell.Connection:
        self._initialize()
        yield self._connection
        self._teardown()


class NopasswdSSHConnection(RemoteShell):
    """
    Assumes the following.

        - ssh is available in your PATH
        - once you've ssh-ed into the given coordinates, you are
        dropped immediately into the shell without asking
        passwords and whatnot

    It does not support error handling on itself.

    It floods the commands, cannot detect if one is finished.
    """

    def __init__(self, coordinates: str):
        super().__init__()
        self.coordinates = coordinates
        self.sshProcess = None
        self.readerThread = None

    def _initialize(self):
        self.sshProcess = subprocess.Popen(
            ['ssh', '-tt', self.coordinates],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=0
        )

        self.readerThread = Process(target=self._readOutput, args=())
        self.readerThread.start()

    def _teardown(self):
        assert self.sshProcess
        # print("Closing connection")
        self.sshProcess.stdin.write("exit\n")
        self.sshProcess.stdin.close()

    def _writeCmd(self, cmd: List[str]):
        assert self.sshProcess
        cmd_str = list_of_shell_args_to_str(cmd)
        print("[ssh shell] " + cmd_str)
        self.sshProcess.stdin.write(cmd_str + "\n")

    def _readOutput(self):
        for c in iter(lambda: self.sshProcess.stdout.read(1), ''):
            sys.stdout.write(c)