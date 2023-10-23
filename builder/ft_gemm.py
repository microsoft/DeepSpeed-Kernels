# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team

from .builder import CMakeExtension

class FTGemmBuilder(CMakeExtension):
    def __init__(self, name, sources=[]):
        super().__init__(name, sources)
        
    @property
    def source(self):
        return "dskernels/ft_gemm/gemm_variants/"