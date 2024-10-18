class code():
    def __init__(self):
        self.globalCode=''  #code in the global scope
        self.classes={}     #{name class:[{signature: body},attributes]}
        self.functions={}   #functions {signature: body

cppCodeObject=code()
cppCodeObject.globalCode+='#include "pcppt/codeCpp/FlexibleValue.h"\n\n'

cppSupportClass={'flexType':'FlexibleValue', #class to make array compose to mylty type
    'get':'assignValue','compare':'compare'
}