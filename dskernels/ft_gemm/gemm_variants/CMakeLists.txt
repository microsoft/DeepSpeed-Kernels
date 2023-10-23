# Copyright (c) 2022-2023, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cmake_minimum_required(VERSION 3.11)
project(DeepSpeedFTKernels CXX CUDA)

Set(CMAKE_CXX_STANDARD 17)
Set(CMAKE_CUDA_STANDARD 17)

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})

if (NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
    file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/v0.16.1/conan.cmake"
                "${CMAKE_BINARY_DIR}/conan.cmake"
                EXPECTED_HASH SHA256=396e16d0f5eabdc6a14afddbcfff62a54a7ee75c6da23f32f7a31bc85db23484
                TLS_VERIFY ON)
endif()

find_package(CUDA)

if (NOT WIN32)
    list(APPEND CMAKE_CXX_FLAGS "-fmax-errors=1 -Wfatal-errors")
    Set(LIB_NAME "deepspeedft")
else()
    Set(LIB_NAME "libdeepspeedft")
endif()

list(APPEND NVCC_FLAGS "-O3")
list(APPEND NVCC_FLAGS "-U__CUDA_NO_HALF_OPERATORS__")
list(APPEND NVCC_FLAGS "-U__CUDA_NO_HALF_CONVERSIONS__")
list(APPEND NVCC_FLAGS "-U__CUDA_NO_HALF2_OPERATORS__")
list(APPEND NVCC_FLAGS "-U__CUDA_NO_BFLOAT16_CONVERSIONS__")
list(APPEND NVCC_FLAGS "-U__CUDA_NO_BFLOAT16_OPERATORS__")
list(APPEND NVCC_FLAGS "-expt-relaxed-constexpr")
list(APPEND NVCC_FLAGS "--use_fast_math")
add_definitions(-DENABLE_BF16)
add_definitions(-DBUILD_CUTLASS_MOE)
add_definitions(-DBUILD_CUTLASS_MIXED_GEMM)

add_library(cutlass_heuristic STATIC utils/cutlass_heuristic.cc)
target_include_directories(cutlass_heuristic PRIVATE
    ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../third_party/cutlass/include)
set_property(TARGET cutlass_heuristic PROPERTY POSITION_INDEPENDENT_CODE ON)
target_compile_options(cutlass_heuristic PRIVATE $<$<COMPILE_LANGUAGE:CUDA>:${NVCC_FLAGS}>)

add_library(cutlass_preprocessors STATIC utils/cutlass_preprocessors.cc)
target_include_directories(cutlass_preprocessors PRIVATE
    ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../third_party/cutlass/include)
set_property(TARGET cutlass_preprocessors PROPERTY POSITION_INDEPENDENT_CODE ON)
target_compile_options(cutlass_preprocessors PRIVATE $<$<COMPILE_LANGUAGE:CUDA>:${NVCC_FLAGS}>)

set(VERBOSE_BUILD 0)

if (VERBOSE_BUILD)
    list(APPEND NVCC_FLAGS "--ptxas-options=-v")
endif()

add_library(${LIB_NAME} SHARED)

set(moe_gemm_files "")
file(GLOB moe_gemm_files ${moe_gemm_files} moe_gemm/*.cu)
set(fpA_intB_files "")
file(GLOB fpA_intB_files ${fpA_intB_files} fpA_intB_gemm/*.cu)

set(ALL_SRCS ${moe_gemm_files} ${fpA_intB_files})

target_sources(${LIB_NAME} PRIVATE ${ALL_SRCS})
target_include_directories(${LIB_NAME} PRIVATE
    ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../third_party/cutlass/include)
set_property(TARGET ${LIB_NAME} PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET ${LIB_NAME} PROPERTY CUDA_RESOLVE_DEVICE_SYMBOLS ON)
target_link_libraries(${LIB_NAME} PRIVATE cutlass_heuristic)

target_compile_options(${LIB_NAME} PRIVATE $<$<COMPILE_LANGUAGE:CUDA>:${NVCC_FLAGS}>)
set_target_properties(${LIB_NAME} PROPERTIES CUDA_ARCHITECTURES "${CUDA_ARCH_LIST}")
set_target_properties(${LIB_NAME} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${LIB_OUTPUT_DIR})

# Show timings?
set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE "${CMAKE_COMMAND} -E time")
