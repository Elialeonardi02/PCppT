/* DaCe AUTO-GENERATED FILE. DO NOT MODIFY */
#include <dace/dace.h>
#include "../../include/hash.h"

struct sumParallelArrays_state_t {
    dace_fpga_context *fpga_context;
};



DACE_EXPORTED void __dace_runstate_0_sumParallelArrays_0(sumParallelArrays_state_t *__state, hlslib::ocl::Buffer<int, hlslib::ocl::Access::readWrite> &fpga___return, hlslib::ocl::Buffer<int, hlslib::ocl::Access::readWrite> &fpga_a, hlslib::ocl::Buffer<int, hlslib::ocl::Access::readWrite> &fpga_b, hlslib::ocl::Buffer<int, hlslib::ocl::Access::readWrite> &fpga_r);

void __program_sumParallelArrays_internal(sumParallelArrays_state_t*__state, int * __restrict__ __return, int * __restrict__ a, int * __restrict__ b, int * __restrict__ r)
{
    hlslib::ocl::Buffer <int, hlslib::ocl::Access::readWrite> fpga_a;
    fpga_a = __state->fpga_context->Get().MakeBuffer<int, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, 0, 6);
    hlslib::ocl::Buffer <int, hlslib::ocl::Access::readWrite> fpga_b;
    fpga_b = __state->fpga_context->Get().MakeBuffer<int, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, 1, 6);
    hlslib::ocl::Buffer <int, hlslib::ocl::Access::readWrite> fpga_r;
    fpga_r = __state->fpga_context->Get().MakeBuffer<int, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, 2, 6);
    hlslib::ocl::Buffer <int, hlslib::ocl::Access::readWrite> fpga___return;
    fpga___return = __state->fpga_context->Get().MakeBuffer<int, hlslib::ocl::Access::readWrite>(hlslib::ocl::StorageType::DDR, 3, 6);

    {

        fpga_a.CopyFromHost(0, 6, a);
        fpga_b.CopyFromHost(0, 6, b);
        fpga_r.CopyFromHost(0, 6, r);
        fpga___return.CopyFromHost(0, 6, __return);

    }
    {
        __dace_runstate_0_sumParallelArrays_0(__state, fpga___return, fpga_a, fpga_b, fpga_r);

    }
    {

        fpga_r.CopyToHost(0, 6, r);
        fpga___return.CopyToHost(0, 6, __return);

    }
}

DACE_EXPORTED void __program_sumParallelArrays(sumParallelArrays_state_t *__state, int * __restrict__ __return, int * __restrict__ a, int * __restrict__ b, int * __restrict__ r)
{
    __program_sumParallelArrays_internal(__state, __return, a, b, r);
}
DACE_EXPORTED int __dace_init_xilinx(sumParallelArrays_state_t *__state);

DACE_EXPORTED sumParallelArrays_state_t *__dace_init_sumParallelArrays()
{
    int __result = 0;
    sumParallelArrays_state_t *__state = new sumParallelArrays_state_t;


    __result |= __dace_init_xilinx(__state);

    if (__result) {
        delete __state;
        return nullptr;
    }
    return __state;
}

DACE_EXPORTED int __dace_exit_sumParallelArrays(sumParallelArrays_state_t *__state)
{
    int __err = 0;
    delete __state;
    return __err;
}

