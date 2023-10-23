# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team

import os
from setuptools import Extension
from setuptools.command.build_ext import build_ext
import subprocess


class CMakeExtension(Extension):
    def __init__(self, name, sources=[]):
        super().__init__(name, sources)


class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
       abs_build_temp = os.path.abspath(self.build_temp)
       abs_build_temp = os.path.join(abs_build_temp, ext.name)
       subprocess.check_call(['cmake', '-B', abs_build_temp], cwd=ext.source)
       subprocess.check_call(['make', '-j'], cwd=abs_build_temp)
