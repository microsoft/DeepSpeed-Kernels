
#pragma once

#include <cstdint>
#include "cuda.h"
#include "cute/pointer.hpp"

struct __align__(32) AttentionAtom {
    int32_t* block_idx_list;

    int q_start_idx;
    int q_len;
    int kv_blocks;
    int kv_remainder;
    int global_q_idx;
    int allocation_group_offset;

    template <int threads>
    __device__ void load_kv_block_idxs(cute::smem_ptr<int32_t> block_idx_list_shr, int tidx) const
    {
        for (int i = tidx; i < kv_blocks; i += threads) { block_idx_list_shr[i] = i; }
        // Aggressive (but safe) sync
        __syncthreads();
    }
};
