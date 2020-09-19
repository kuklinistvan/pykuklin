from __future__ import annotations

from .common import list_of_shell_args_to_str

from typing import List
import subprocess
import sys
from contextlib import contextmanager
from multiprocessing import Process


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
        self.sshProcess.stdin.write("exit\n")
        self.sshProcess.stdin.close()

    def _writeCmd(self, cmd: List[str]):
        assert self.sshProcess
        cmd_str = list_of_shell_args_to_str(cmd)
        self.sshProcess.stdin.write(cmd_str + "\n")

    def _readOutput(self):
        for c in iter(lambda: self.sshProcess.stdout.read(1), ''):
            sys.stdout.write(c)