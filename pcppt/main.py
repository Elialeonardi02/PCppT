import ast

from pcppt import astToCpp, pythonToAST, codeCppClass as cppc
import sys
import subprocess
import inspect

from pcppt.wireflowOperators import FOperatorKind


def generator_cpp_code(astG, operator=FOperatorKind.NONE):

    import ast  # TODO remove, use for debugging
    print(ast.dump(astG, indent=4))  # TODO remove, use for debugging
    astToCpp.generateAstToCppCode(astG, operator)
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


if __name__ == "__main__":  #transpiling file
    if len(sys.argv) != 3:
        print("Usage: <path_python_script>.py  <path_cpp_destination_file>.cpp")
        sys.exit(1)

    source = sys.argv[1]  # source python
    file_path_destination = sys.argv[2]  # destination c++
    codeCpp = generator_cpp_code(pythonToAST.generateAstFromFile(source))

    print(codeCpp)  # TODO remove, use for debugging
    with open(file_path_destination, "w") as file:
        file.write(codeCpp)

    # compile to check sintax of the c++ code
    subprocess.run(["g++", "-c", file_path_destination, "-fconcepts", "-o", file_path_destination[:-4]])

def python_cpp_transpiling(func,operator=FOperatorKind.NONE):   #transpilling string code
    func_code=inspect.getsource(func)
    if func.__name__!='<lambda>':  #is a function or a class
        func_code=f"@wireflow\n{func_code}"
    astG = ast.parse(func_code)
    return generator_cpp_code(astG, operator)