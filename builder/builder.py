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
        # Build in kernel unique sub-directory inside temp build directory
        abs_build_temp = os.path.abspath(self.build_temp)
        abs_build_temp = os.path.join(abs_build_temp, ext.name)

        # Pass through CUDA_ARCH_LIST if defined, otherwise fall back to native
        cuda_arch_list = os.environ.get('CUDA_ARCH_LIST', 'native')

        # Destination path for final binaries
        abs_build_lib = os.path.join(os.path.abspath(self.build_lib), "dskernels")

        subprocess.check_call(['cmake',
                               '-B', abs_build_temp,
                               f'-DLIB_OUTPUT_DIR={abs_build_lib}',
                               f'-DCUDA_ARCH_LIST={cuda_arch_list}'],
                               cwd=ext.source)
        subprocess.check_call(['make', '-j'], cwd=abs_build_temp)
