class code():
    def __init__(self):
        self.globalCode=''  #code in the global scope
        self.classes={}     #{name class:{protected:{'attributes':[],'methods':{}}.private: {'attributes':[],'methods':{}},public: {'attributes':[],'methods':{}}}
        self.functions={}   #functions {signature: body

cppCodeObject=code()
def reset_cppCodeObject(): #FIXME incapsulate cppCOdeObject in a object 
    global cppCodeObject
    cppCodeObject=code()
cppCodeObject.globalCode+="#include <ostream>\n" #use to generate method for user debugging #FIXME use ore remove?