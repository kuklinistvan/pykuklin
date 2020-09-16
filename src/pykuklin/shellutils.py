# from subprocess import call
# from typing import List

# def shell(args: List[str]):
#     assert 0 == call([args])

from contextlib import contextmanager
from pathlib import Path
import os
from typing import List

import subprocess

@contextmanager
def working_directory(path: Path) -> None:
    prev_dir = os.getcwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(prev_dir)


def shell(cmd: List[str]) -> None:
    args_with_apostroves_where_necessary = []

    for e in cmd:
        if e.find(' ') == -1:
            args_with_apostroves_where_necessary.append(e)
        else:
            args_with_apostroves_where_necessary.append('"' + e + '"')

    print("[shell] " + " ".join(args_with_apostroves_where_necessary), flush=True)

    assert 0 == subprocess.call(cmd)