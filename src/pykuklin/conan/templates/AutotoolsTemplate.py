from pykuklin.downloader import get_downloader_available_in_current_environment
from pykuklin.conan.tools import ldflags2ld_library_path, build_env_vars_set

from conans import ConanFile, AutoToolsBuildEnvironment
from conans.tools import environment_append
from pathlib import Path
from contextlib import contextmanager

import ipdb

class AutotoolsTemplate(ConanFile):
    # Example:
    settings = "os", "compiler", "build_type", "arch"
    archive_format_file_suffix = ".tar.gz"

    archive_url_prefix: str

    # Can be auto-configured with setup_template_vars:
    topdir: str
    archive: str

    def __init__(self, output, runner, display_name="", user=None, channel=None):
        super().__init__(output, runner, display_name, user, channel)
        self.configure_additional_args = ['--enable-static']

    def configure(self):
        self.setup_template_vars()


    def setup_template_vars(self):
        """
        Auto configures topdir and archive file name.
        """
        self.topdir = self.name + "-" + self.version
        self.archive = self.topdir + self.archive_format_file_suffix

    def source(self):
        get_downloader_available_in_current_environment()(self.archive_url_prefix + self.archive, Path(self.archive))
        self.run("tar xvf " + self.archive)

    def build(self):
        print("Building in package() phase.")

    def package(self):       
        autotools = AutoToolsBuildEnvironment(self)

        # with add_rpath_to_ldflags(autotools):
        with build_env_vars_set(self, append_libdirs_to_rpath = True):
            autotools.configure(configure_dir=self.topdir, args=self.configure_additional_args)
            autotools.make(target=self.topdir)
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = [self.name]


# @contextmanager
# def add_rpath_to_ldflags(autotools_build_env: AutoToolsBuildEnvironment) -> None:
#     env = autotools_build_env.vars

#     library_dirs_commasep = ldflags2ld_library_path(env['LDFLAGS'])
#     env['LDFLAGS'] = env['LDFLAGS'] + ' -Wl,--rpath=' + library_dirs_commasep

#     with environment_append(env):
#         yield


# class GnuHello(AutotoolsTemplate):
