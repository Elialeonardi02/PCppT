import astToCpp
import pythonToAST
import sys
import subprocess

import codeCpp.codeCppClass as cppc

#pragmas
def applyHLSInline(func_code,):  #FIXME pragma hls inline test
    if func.count('\n') <= 5:
        i=func_code.find('\n')
        func_code=f"{func_code[:i+1]}  #pragma HLS inline\n{func_code[i+1:]}"
    return func_code

if len(sys.argv) != 3:
    print("Usage: <path_python_script>.py  <path_cpp_destination_file>.cpp")
    sys.exit(1)

file_path_source = sys.argv[1] #source python
file_path_destination= sys.argv[2]  #destination c++

astG, comment = pythonToAST.generateAstComments(file_path_source)

import ast                      #TODO remove, use for debugging
print(ast.dump(astG, indent=4)) #TODO remove, use for debugging

astToCpp.generateAstToCppCode(astG)
codeCpp=cppc.cppCodeObject.globalCode
if cppc.cppCodeObject.classes!={}:
    for cls in cppc.cppCodeObject.classes:
        if 'private' not in cppc.cppCodeObject.classes[cls] and 'protected' not in cppc.cppCodeObject.classes[cls]:
            codeCpp+='struct '+cls+'{\n'
            for elm in cppc.cppCodeObject.classes[cls]['public']['attributes']:
                codeCpp += f"{elm}\n"
            for sig, func in  cppc.cppCodeObject.classes[cls]['public']['methods'].items():
                #func=applyHLSInline(func)# FIXME pragma hls inline test
                codeCpp += f"{sig} \n{func}\n"
        else:
            codeCpp+='class '+cls+'{\n'
            for vis,elms in cppc.cppCodeObject.classes[cls].items():
                codeCpp+=f"{vis}:\n"
                for elm in elms['attributes']:
                    codeCpp+=f"{elm}\n"
                for sig,func in elms['methods'].items():
                    #func=applyHLSInline(func)# FIXME pragma hls inline test
                    codeCpp += f"{sig} \n{func}\n"
        codeCpp+='};\n'
for sign in cppc.cppCodeObject.functions:
    codeCpp+=sign+';\n\n'
for sign_fun in cppc.cppCodeObject.functions:
    #func=applyHLSInline(cppc.cppCodeObject.functions[sign_fun])# FIXME pragma hls inline test
    codeCpp+=f"{sign_fun}\n{func}\n"

print(codeCpp)  #TODO remove, use for debugging
with open(file_path_destination, "w") as file:
    file.write(codeCpp)

# compile to check sintax of the c++ code
subprocess.run(["g++", "-c", file_path_destination,"-fconcepts", "-o", file_path_destination[:-4]])
