// Copyright (c) Microsoft Corporation.
// SPDX-License-Identifier: Apache-2.0

// DeepSpeed Team

#pragma once

/*
NOTE(cmikeh2): This needs to match the equivalent file in deepspeed/csrc/includes
exactly to ensure coherence.
*/

enum ActivationType {
    GELU = 0,
    RELU = 1,
    SILU = 2,
    GEGLU = 3,
    ReGLU = 4,
    SiGLU = 5,
    IDENTITY = 6,
    InvalidType = -1
};

inline bool isGatedActivation(ActivationType activation_type)
{
    return activation_type == ActivationType::GEGLU || activation_type == ActivationType::ReGLU
           || activation_type == ActivationType::SiGLU;
}
