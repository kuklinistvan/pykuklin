from pykuklin.downloader import get_downloader_available_in_current_environment

from conans import ConanFile, AutoToolsBuildEnvironment, RunEnvironment, tools
from pathlib import Path
import os

class AutotoolsTemplate(ConanFile):
    # Example:
    settings = "os", "compiler", "build_type", "arch"
    archive_format_file_suffix = ".tar.gz"

    archive_url_prefix: str

    # Can be auto-configured with setup_template_vars:
    topdir: str
    archive: str

    configure_additional_args = None

    def configure(self):
        self.setup_template_vars()

    def setup_template_vars(self):
        """
        Auto configures topdir and archive file name.
        """
        self.topdir = str(self.name) + "-" + str(self.version)
        self.archive = str(self.topdir) + str(self.archive_format_file_suffix)

    def source(self):
        get_downloader_available_in_current_environment()(self.archive_url_prefix + self.archive, Path(self.archive))
        self.run("tar xvf " + self.archive)

    def build(self):
        print("Building in package() phase.")

    def package(self):
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(configure_dir=self.topdir, args=self.configure_additional_args)
            autotools.make(target=self.topdir)
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = [self.name]

