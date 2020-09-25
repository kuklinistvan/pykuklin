#!/usr/bin/env python3

import click

@click.group()
def cli_entry():
    """
    Common routines, shortcuts, algorithms that I frequently use.

    Kuklin István Alexander - www.codekuklin.com

    Licensed for you under the terms of the Apache License 2.0.
    
    For the license text and for the dependent libraries please visit the repository at
    https://github.com/kuklinistvan/pykuklin/
    """
    pass

from .gitignore import *

if __name__ == "__main__":
    cli_entry()