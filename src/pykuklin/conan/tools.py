from pykuklin.shellutils.common import with_apostroves_if_necessary

from conans import ConanFile, AutoToolsBuildEnvironment, tools

import pprint
pp = pprint.PrettyPrinter(indent=2)
from contextlib import contextmanager
from typing import List

import re
import os

@contextmanager
def build_env_vars_set(conanfile: ConanFile, libs_as_ldflags = False, append_libdirs_to_ld_library_path = False, append_libdirs_to_rpath = False, cxxflags_to_cflags=False):
    try:
        env = AutoToolsBuildEnvironment(conanfile).vars
        
        if libs_as_ldflags:
            print("(appending LIBS to LDFLAGS)")
            prev_ldflags = env['LDFLAGS']
            env['LDFLAGS'] = ' '.join([prev_ldflags, env['LIBS']])

        env['LDFLAGS'] += ' -L' + with_apostroves_if_necessary(conanfile.package_folder + "/lib")

        libpaths = ldflags2ld_library_path(env['LDFLAGS'])

        if append_libdirs_to_ld_library_path:
            if 'LD_LIBRARY_PATH' in env:
                env['LD_LIBRARY_PATH'] = ':'.join([libpaths, env['LD_LIBRARY_PATH']])
            else:
                env['LD_LIBRARY_PATH'] = libpaths

        if append_libdirs_to_rpath:
            env['LDFLAGS'] = env['LDFLAGS'] + ' -Wl,--rpath=' + libpaths

        if env['CPPFLAGS'] and env['CXXFLAGS']:
            env['CXXFLAGS'] += ' '
            env['CXXFLAGS'] += env['CPPFLAGS']
            del env['CPPFLAGS']

        if cxxflags_to_cflags:
            env['CFLAGS'] = env['CXXFLAGS']

        print("Setting up environment:")
        pp.pprint(env)

        with tools.environment_append(env):
            yield
    finally:
        print("Tearing down environment")
        # disgusting hack, but only the AutoToolsBuildEnvironment had the
        # routine to create this environment

def ldflags2ld_library_path(ldflags: str) -> List[str]:
    """
    Returns: /path/to/somelib:"/path/to/some spaced/lib/":/path/to/another
    """
    libdirs = extract_libdirs_from_ldflags(ldflags)
    libdirs_comasep = ':'.join(list(map(lambda l: with_apostroves_if_necessary(l), libdirs)))
    return libdirs_comasep

def extract_libdirs_from_ldflags(ldflags: str):
    libdirs_e = re.compile(r"\s+-L(?:(?:([\"'])(.+)(?:\1))|(\S+))")
    libdirs_result = re.findall(libdirs_e, ldflags)
    libdirs = list(map(lambda t: t[1] + t[2], libdirs_result))
    return libdirs