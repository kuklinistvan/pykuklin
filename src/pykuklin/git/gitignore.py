from pykuklin import NotFoundException

import pkgutil
from typing import List
from glob import glob
import os

from pathlib import Path
import yaml

DIR = Path(os.path.dirname(os.path.realpath(__file__))).absolute()

def ls() -> List[str]:
    r = []

    for f in glob(str(DIR / "collection/") + "/*"):
        if not '.' in f:
            r.append(os.path.basename(f))

    return r

def get(template: str) -> str:  
    return pkgutil.get_data(__name__, "collection/" + template).decode('utf-8')

def ls_group() -> List[str]:
    r = []
    
    for e in get_group_parser():
        key = list(e.keys())[0]
        r.append(key)
    
    return r
    
def get_group_members(group: str) -> str:
    for g in get_group_parser():
        current_group_name = list(g.keys())[0]
        if current_group_name == group:
            return list(g.values())[0]

    raise NotFoundException()

def get_group_parser():
    with open(str(DIR / "collection/groups.yaml")) as f:
        parser = yaml.full_load(f.read())
    
    return parser
