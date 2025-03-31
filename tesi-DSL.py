import pcppt
from DSL import operators

# Classe che rappresenta l'input con un valore numerico
class input_t:
    def __init__(self, value: float):
        self.value = value

pcppt.python_cpp_transpiling(input_t)

# Classe che raccoglie i risultati, con un attributo per il risultato finale
class output_t:
    def __init__(self):
        self.result = 0.0  # Attributo per memorizzare il risultato finale

pcppt.python_cpp_transpiling(output_t)

# Operatore di mapping: trasforma l'input applicando una scala e un offset
@operators.FOperator()
class MapOperator:
    def __init__(self, scale: float, offset: float):
        self.scale = scale
        self.offset = offset

    def __call__(self, item: input_t, result: output_t) -> None:
        result.result = item.value * self.scale + self.offset  # Direttamente assegnato al risultato


# Operatore di filtro: se l'input supera una soglia, memorizza il valore in `result`
@operators.FOperator(gather_policy=operators.FDispatchPolicy.KB)
class FilterOperator:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def __call__(self, item, result: output_t, keep: bool):
        if item.value > self.threshold:
            result.result = item.value
            keep = True
        else:
            result.result = 0.0
            keep = False
"""
app = FApplication ('./ myApp' , 'input_t' , target = FDevice.Xilinx )
app.add_source()
app.add ( FOperator ( ’ detector ’ , 2 , FOperatorKind . FILTER ) )

app.generate_code
"""


print(operators.operator_declaration(MapOperator))
print(operators.operator_declaration(FilterOperator))