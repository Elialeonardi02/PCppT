import dace
from dace.transformation.auto import auto_optimize as aopt
N=6
@dace.program
def sumParallelArrays(a: dace.int32[N], b: dace.int32[N], r:dace.int32[N]):
    for i in range(N):
        r[i] = a[i] + b[i]
    return r
# Configura il target per la compilazione FPGA
sdfg = sumParallelArrays.to_sdfg()
aopt.auto_optimize(sdfg, dace.DeviceType.FPGA)
# Compila il SDFG per il target FPGA
compiled_sdfg = sdfg.compile()  # Prova a usare una stringa invece di un attributo
