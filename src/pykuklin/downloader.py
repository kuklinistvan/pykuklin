from pathlib import Path
from subprocess import call
from distutils.spawn import find_executable

def wget(address: str, save_here: Path, wget_invoke = "wget") -> None:
    assert 0 == call([wget_invoke, address, '-O', str(save_here)])

def curl(address: str, save_here: Path, curl_invoke = "curl") -> None:
    assert 0 == call([curl_invoke, address, '-o', str(save_here)])


def get_downloader_available_in_current_environment():
    if find_executable("wget"):
        return wget
    if find_executable("curl"):
        return curl
