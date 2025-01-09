from enum import Enum
#use to identify correct operator
class FOperatorKind(Enum):
    NONE = 1
    FILTER = 3
    MAP = 4
    FLAT_MAP = 5