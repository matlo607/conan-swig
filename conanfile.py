#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
from os import path

class SwigConan(ConanFile):
    name = "swig"
    version = "3.0.12"
    description = """SWIG is a software development tool that connects programs written
                     in C and C++ with a variety of high-level programming languages."""
    license = "https://github.com/swig/swig/blob/master/LICENSE"
    url = "https://github.com/matlo607/conan-swig.git"
    sources = "https://github.com/swig/swig.git"
    source_dir = "{}-{}".format(name, version)
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "tests": [True, False]
    }
    default_options = (
        "tests=False"
    )
    generators = "cmake"

    def source(self):
        self.run("git clone {} {}".format(self.sources, self.source_dir))
        with tools.chdir(path.join(self.source_folder, self.source_dir)):
            self.run("git checkout tags/rel-{version}".format(version=self.version))

    def build_requirements(self):
        if self.options.tests or self.develop:
            self.build_requires("boost/1.66.0@conan/stable")

    def build(self):
        with tools.chdir(path.join(self.source_folder, self.source_dir)):
            args = []
            args.append('--prefix={}'.format(self.package_folder))
            args.append('--without-go')
            args.append('--without-java')
            args.append('--without-perl5')
            args.append('--without-ruby')
            args.append('--with-python=python2')
            args.append('--with-python3=python3')
            if self.options.tests or self.develop:
                args.append('--with-boost={}'.format(self.deps_cpp_info['boost'].rootpath))
            self.run('./autogen.sh')
            env_build = AutoToolsBuildEnvironment(self)
            env_build.configure(args=args)
            env_build.make()
            env_build.make(args=['install'])
            if self.options.tests or self.develop:
                self.output.info("which swig: {}".format(tools.which("swig")))
                self.output.info("which swig3.0: {}".format(tools.which("swig3.0")))
                self.output.info("which ccache-swig: {}".format(tools.which("ccache-swig")))
                self.output.info("which ccache-swig3.0: {}".format(tools.which("ccache-swig3.0")))
                # Unit tests are failing :
                # - GCC 7 not supported: https://github.com/swig/swig/issues/1211
                # - Setting CC makes CCache's test fail: https://github.com/swig/swig/issues/1212
                env_build.make(args=['check'])

    def package(self):
        # already done by make install
        pass

    def package_info(self):
        self.cpp_info.bindirs = ['bin']
        self.cpp_info.resdirs = ['share']
