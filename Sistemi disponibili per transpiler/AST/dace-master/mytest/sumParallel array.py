import dace
N=6
@dace.program
def sumParallelArrays(a: dace.int32[N], b: dace.int32[N], r:dace.int32[N]):
    for i in range(N):
        r[i] = a[i] + b[i]
    return r
# Configura il target per la compilazione FPGA
sdfg = sumParallelArrays.to_sdfg()

# Compila il SDFG per il target FPGA
compiled_sdfg = sdfg.compile('intel_fpga.cpp')  # Prova a usare una stringa invece di un attributo

# Controlla la configurazione corrente per verificare che sia stata impostata correttamente
current_config = dace.config.Config.get('compiler')
print("Configurazione attuale:", current_config)