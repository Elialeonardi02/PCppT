#include <dace/dace.h>
typedef void * sumParallelArraysHandle_t;
extern "C" sumParallelArraysHandle_t __dace_init_sumParallelArrays();
extern "C" int __dace_exit_sumParallelArrays(sumParallelArraysHandle_t handle);
extern "C" void __program_sumParallelArrays(sumParallelArraysHandle_t handle, int * __restrict__ __return, int * __restrict__ a, int * __restrict__ b, int * __restrict__ r);
