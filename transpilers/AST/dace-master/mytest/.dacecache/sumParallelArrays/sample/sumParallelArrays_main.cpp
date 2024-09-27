#include <cstdlib>
#include "../include/sumParallelArrays.h"

int main(int argc, char **argv) {
    sumParallelArraysHandle_t handle;
    int err;
    int * __restrict__ __return = (int*) calloc(6, sizeof(int));
    int * __restrict__ a = (int*) calloc(6, sizeof(int));
    int * __restrict__ b = (int*) calloc(6, sizeof(int));
    int * __restrict__ r = (int*) calloc(6, sizeof(int));


    handle = __dace_init_sumParallelArrays();
    __program_sumParallelArrays(handle, __return, a, b, r);
    err = __dace_exit_sumParallelArrays(handle);

    free(__return);
    free(a);
    free(b);
    free(r);


    return err;
}
