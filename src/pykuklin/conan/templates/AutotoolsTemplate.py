from conans import ConanFile, AutoToolsBuildEnvironment


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
        self.topdir = self.name + "-" + self.version
        self.archive = self.topdir + self.archive_format_file_suffix

    def source(self):
        self.run("wget \"{}\"".format(self.archive_url_prefix + self.archive))
        self.run("tar xvf " + self.archive)

    def build(self):
        print("Building in package() phase.")

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir=self.topdir, args=self.configure_additional_args)
        autotools.make(target=self.topdir)
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = [self.name]


# class GnuHello(AutotoolsTemplate):
