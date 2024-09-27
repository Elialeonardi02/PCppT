#include "dace/xilinx/host.h"
#include "dace/dace.h"
#include "dace/xilinx/stream.h"



struct sumParallelArrays_state_t {
    dace_fpga_context *fpga_context;
};


DACE_EXPORTED int __dace_init_xilinx(sumParallelArrays_state_t *__state) {
    dace::unset_environment_variable("XCL_EMULATION_MODE");
    dace::unset_environment_variable("XILINX_SDX");
    dace::unset_environment_variable("EMCONFIG_PATH");
    
    
    __state->fpga_context = new dace_fpga_context();
    __state->fpga_context->Get().MakeProgram(DACE_BINARY_DIR "/sumParallelArrays_hw.xclbin");
    return 0;
}

DACE_EXPORTED int __dace_exit_xilinx(sumParallelArrays_state_t *__state) {
    delete __state->fpga_context;
    return 0;
}

///////////////////////////////////////////////////////////////////////////////
// Kernel: sumParallelArrays_0_0
///////////////////////////////////////////////////////////////////////////////

// Signature of kernel function (with raw pointers) for argument matching
DACE_EXPORTED void sumParallelArrays_0_0(int * __restrict__ fpga___return_0, int * __restrict__ fpga_a_0, int * __restrict__ fpga_b_0, int * __restrict__ fpga_r_0);

DACE_EXPORTED void __dace_runstate_0_sumParallelArrays_0(sumParallelArrays_state_t *__state, hlslib::ocl::Buffer<int, hlslib::ocl::Access::readWrite> &fpga___return, hlslib::ocl::Buffer<int, hlslib::ocl::Access::readWrite> &fpga_a, hlslib::ocl::Buffer<int, hlslib::ocl::Access::readWrite> &fpga_b, hlslib::ocl::Buffer<int, hlslib::ocl::Access::readWrite> &fpga_r) {
    hlslib::ocl::Program program = __state->fpga_context->Get().CurrentlyLoadedProgram();
    std::vector<hlslib::ocl::Event> all_events;
    auto sumParallelArrays_0_0_kernel = program.MakeKernel(sumParallelArrays_0_0, "sumParallelArrays_0_0", fpga___return, fpga_a, fpga_b, fpga_r);
    hlslib::ocl::Event sumParallelArrays_0_0_event = sumParallelArrays_0_0_kernel.ExecuteTaskAsync();
    all_events.push_back(sumParallelArrays_0_0_event);
    hlslib::ocl::WaitForEvents(all_events);
}


