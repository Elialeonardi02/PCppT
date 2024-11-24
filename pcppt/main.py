import astToCpp
import pythonToAST
import sys
import subprocess

import codeCpp.codeCppClass as cppc

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
            if 'public' in cppc.cppCodeObject.classes[cls] and 'attributes' in cppc.cppCodeObject.classes[cls]['public']:
                for elm in cppc.cppCodeObject.classes[cls]['public']['attributes']:
                    codeCpp += f"{elm}\n"
            if 'public' in cppc.cppCodeObject.classes[cls] and 'methods' in cppc.cppCodeObject.classes[cls]['public']:
                for sig, func in  cppc.cppCodeObject.classes[cls]['public']['methods'].items():
                    codeCpp += f"{sig} \n{func}\n"
        else:
            codeCpp+='class '+cls+'{\n'
            for vis,elms in cppc.cppCodeObject.classes[cls].items():
                codeCpp+=f"{vis}:\n"
                for elm in elms['attributes']:
                    codeCpp+=f"{elm}\n"
                for sig,func in elms['methods'].items():
                    codeCpp += f"{sig} \n{func}\n"
        codeCpp+='};\n'
for sign in cppc.cppCodeObject.functions:
    codeCpp+=sign+';\n\n'
for sign_fun, func in cppc.cppCodeObject.functions.items():
    codeCpp+=f"{sign_fun}\n{func}\n"

print(codeCpp)  #TODO remove, use for debugging
with open(file_path_destination, "w") as file:
    file.write(codeCpp)

# compile to check sintax of the c++ code
subprocess.run(["g++", "-c", file_path_destination,"-fconcepts", "-o", file_path_destination[:-4]])
