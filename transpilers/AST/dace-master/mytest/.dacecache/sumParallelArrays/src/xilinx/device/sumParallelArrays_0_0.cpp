//#include <dace/fpga_device.h>
#include <dace/math.h>
#include <dace/complex.h>

struct sumParallelArrays_state_t {
    dace_fpga_context *fpga_context;
};


void loop_body_1_0_0(const int* a, const int* b, int* r) {
    //#pragma HLS INLINE
    int __tmp0;
    int __tmp1;


    __tmp0 = a[0];
    __tmp1 = b[0];
    {
        {
            int __out;

            ///////////////////
            // Tasklet code (assign_7_8)
            __out = (__tmp0 + __tmp1);
            ///////////////////

            *(r + 0) = __out;
        }

    }
    
}

void sumParallelArrays_0_0_0(const int* ____return_in, const int* __a_in, const int* __b_in, const int* __r_in, int* ____return_out, int* __r_out) {
    //#pragma HLS INLINE

    {
        {
            for (int i = 0; i < 6; i += 1) {
                //#pragma HLS PIPELINE II=1
                //#pragma HLS LOOP_FLATTEN
                loop_body_1_0_0(&__a_in[0], &__b_in[0], &__r_out[0]);
            }
        }
        for (int __dace_copy0 = 0; __dace_copy0 < 6; ++__dace_copy0) {
            //#pragma HLS PIPELINE II=1
            //#pragma HLS LOOP_FLATTEN
            dace::Write<int, 1>(____return_out + __dace_copy0, dace::Read<int, 1>(__r_out + __dace_copy0));
        }

    }
    
}

/*void module_sumParallelArrays_0_0(int *fpga___return, int *fpga_a, int *fpga_b, int *fpga_r) {

    sumParallelArrays_0_0_0(&fpga___return[0], &fpga_a[0], &fpga_b[0], &fpga_r[0], &fpga___return[0], &fpga_r[0]);
}

DACE_EXPORTED void sumParallelArrays_0_0(int *fpga___return_0, int *fpga_a_0, int *fpga_b_0, int *fpga_r_0) {
    #pragma HLS INTERFACE m_axi port=fpga___return_0 offset=slave bundle=gmem0
    #pragma HLS INTERFACE m_axi port=fpga_a_0 offset=slave bundle=gmem1
    #pragma HLS INTERFACE m_axi port=fpga_b_0 offset=slave bundle=gmem2
    #pragma HLS INTERFACE m_axi port=fpga_r_0 offset=slave bundle=gmem3
    #pragma HLS INTERFACE s_axilite port=fpga___return_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga_a_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga_b_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=fpga_r_0 bundle=control
    #pragma HLS INTERFACE s_axilite port=return bundle=control
    
    #pragma HLS DATAFLOW
    
    HLSLIB_DATAFLOW_INIT();
    HLSLIB_DATAFLOW_FUNCTION(module_sumParallelArrays_0_0, fpga___return_0, fpga_a_0, fpga_b_0, fpga_r_0);
    HLSLIB_DATAFLOW_FINALIZE();
}*/
