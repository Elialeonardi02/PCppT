class code():
    def __init__(self):
        self.globalCode=''  #code in the global scope
        self.classes={}     #{name class:[{signature: body},attributes]}
        self.functions={}   #functions {signature: body

cppCodeObject=code()
cppCodeObject.globalCode+='#include "../pcppt/codeCpp/FlexibleValue.h"\n#include "../pcppt/codeCpp/ArrayMap.h"\n'

cppSupportClass={'flexType':'FlexibleValue', #class to make array compose to multy type
    'get':'assignValue','compare':'compare', 'set':'setValue',
    'dict':'ArrayMap','dictStruct':'KeyValuePair','mapInsert':'insert', 'mapSearch':'search'
}