import pprint
pp = pprint.PrettyPrinter(indent=2)
from contextlib import contextmanager
from conans import ConanFile, AutoToolsBuildEnvironment, tools

@contextmanager
def build_env_vars_set(conanfile: ConanFile, libs_as_ldflags = False):
    try:
        env = AutoToolsBuildEnvironment(conanfile).vars
        
        if libs_as_ldflags:
            print("(appending LIBS to LDFLAGS)")
            prev_ldflags = env['LDFLAGS']
            env['LDFLAGS'] = ' '.join([prev_ldflags, env['LIBS']])

        print("Setting up environment:")
        pp.pprint(env)

        with tools.environment_append(AutoToolsBuildEnvironment(conanfile).vars):
            yield
    finally:
        print("Tearing down environment")
        # disgusting hack, but only the AutoToolsBuildEnvironment had the
        # routine to create this environment