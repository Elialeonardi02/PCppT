/* DaCe AUTO-GENERATED FILE. DO NOT MODIFY */
#include <dace/dace.h>
#include "../../include/hash.h"

struct sumParallelArrays_state_t {

};

void __program_sumParallelArrays_internal(sumParallelArrays_state_t*__state, int * __restrict__ __return, int * __restrict__ a, int * __restrict__ b, int * __restrict__ r)
{
    long long i;
    int __tmp0;
    int __tmp1;




    for (i = 0; (i < 6); i = (i + 1)) {

        __tmp0 = a[i];
        __tmp1 = b[i];
        {

            {
                int __out;

                ///////////////////
                // Tasklet code (assign_6_8)
                __out = (__tmp0 + __tmp1);
                ///////////////////

                r[i] = __out;
            }

        }

    }
    {


        dace::CopyND<int, 1, false, 6>::template ConstDst<1>::Copy(
        r, __return, 1);

    }
}

DACE_EXPORTED void __program_sumParallelArrays(sumParallelArrays_state_t *__state, int * __restrict__ __return, int * __restrict__ a, int * __restrict__ b, int * __restrict__ r)
{
    __program_sumParallelArrays_internal(__state, __return, a, b, r);
}

DACE_EXPORTED sumParallelArrays_state_t *__dace_init_sumParallelArrays()
{
    int __result = 0;
    sumParallelArrays_state_t *__state = new sumParallelArrays_state_t;



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

