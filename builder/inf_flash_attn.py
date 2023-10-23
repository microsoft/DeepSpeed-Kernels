# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team

from .builder import CMakeExtension

class BlockedFlashBuilder(CMakeExtension):
    def __init__(self, name, sources=[]):
        super().__init__(name, sources)
        
    @property
    def source(self):
        return "dskernels/inf_flash_attn/blocked_flash/"