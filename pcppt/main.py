import ast
import os

from pcppt import astToCpp, codeCppClass as cppc
import sys
import subprocess
import inspect

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def generator_cpp_code(astG, custom_visit={}):
    print(ast.dump(astG, indent=4))  # TODO remove, use for debugging
    astToCpp.generateAstToCppCode(astG, custom_visit)
    codeCpp = cppc.cppCodeObject.globalCode
    if cppc.cppCodeObject.classes != {}:
        for cls in cppc.cppCodeObject.classes:
            if 'private' not in cppc.cppCodeObject.classes[cls] and 'protected' not in cppc.cppCodeObject.classes[cls]:
                codeCpp += 'struct ' + cls + '{\n'
                if 'public' in cppc.cppCodeObject.classes[cls] and 'attributes' in cppc.cppCodeObject.classes[cls][
                    'public']:
                    for elm in cppc.cppCodeObject.classes[cls]['public']['attributes']:
                        codeCpp += f"{elm}\n"
                if 'public' in cppc.cppCodeObject.classes[cls] and 'methods' in cppc.cppCodeObject.classes[cls][
                    'public']:
                    for sig, func in cppc.cppCodeObject.classes[cls]['public']['methods'].items():
                        codeCpp += f"{sig} \n{func}\n"
            else:
                codeCpp += 'class ' + cls + '{\n'
                for vis, elms in cppc.cppCodeObject.classes[cls].items():
                    codeCpp += f"{vis}:\n"
                    for elm in elms['attributes']:
                        codeCpp += f"{elm}\n"
                    for sig, func in elms['methods'].items():
                        codeCpp += f"{sig} \n{func}\n"
            codeCpp += '};\n'
    #for sign in cppc.cppCodeObject.functions: #FIXME can be remove, cause duplicate error on default value for parameters, forces the user to respect the correct order in function definitions
        #codeCpp += sign + ';\n\n'
    for sign_fun, func in cppc.cppCodeObject.functions.items():
        codeCpp += f"{sign_fun}\n{func}\n"
    return codeCpp

def main():
    if len(sys.argv) != 3:
        print("Usage: <path_python_script>.py  <path_cpp_destination_file>.cpp")
        sys.exit(1)

    source = sys.argv[1]  # source python
    file_path_destination = sys.argv[2]  # destination c++
    with open(source, "r") as file:  # FIXME exception when there is no file?
        source_code = file.read()
    codeAst = ast.parse(source_code)

    codeCpp = generator_cpp_code(codeAst)

    print(codeCpp)  # TODO remove, use for debugging
    with open(file_path_destination, "w") as file:
        file.write(codeCpp)

    # compile to check sintax of the c++ code
    subprocess.run(["g++", "-c", file_path_destination, "-fconcepts", "-o", file_path_destination[:-4]])


if __name__ == "__main__":  #transpiling file
    main()
def python_cpp_transpiling(func,custom_visit={}):   #transpilling string code
    return generator_cpp_code(get_ast_from_code(func),custom_visit)

def ast_cpp_transpiling(astG,custom_visit={}): #direct transpiling ast to cpp
    return generator_cpp_code(astG,custom_visit)

def get_ast_from_code(code):
    code=inspect.getsource(code)
    astG=ast.parse(code)
    if isinstance(astG.body[0], ast.FunctionDef) or isinstance(astG.body[0], ast.ClassDef):
        astG.body[0].decorator_list.append(ast.Name(id="transpile", ctx=ast.Load()))
    return astG