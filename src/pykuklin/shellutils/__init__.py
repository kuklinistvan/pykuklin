from .common import list_of_shell_args_to_str

from contextlib import contextmanager
from pathlib import Path
import os
import subprocess

from typing import List


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