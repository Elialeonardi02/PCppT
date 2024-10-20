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
print("Commented AST:")         #TODO remove, use for debugging
print(ast.dump(astG, indent=4)) #TODO remove, use for debugging

astToCpp.generateAstToCppCode(astG)
codeCpp=cppc.cppCodeObject.globalCode
if cppc.cppCodeObject.classes!={}:
    for cls in cppc.cppCodeObject.classes:
        codeCpp+='class '+cls+'{\n'
        for cli in cppc.cppCodeObject.classes[cls][1:]:
            codeCpp+=cli
        for sign in cppc.cppCodeObject.classes[cls][0]:
            codeCpp += sign + cppc.cppCodeObject.classes[cls][0][sign]
    codeCpp+='};\n'
for sign in cppc.cppCodeObject.functions:
    codeCpp+=sign+';\n\n'
for sign_fun in cppc.cppCodeObject.functions:
    codeCpp+=sign_fun+'\n'+cppc.cppCodeObject.functions[sign_fun]+'\n'

print(codeCpp)  #TODO remove, use for debugging
#add comments
"""
for ic in range(0, len(comment)):
    comment_line=comment[ic].start_position[0]  #line start comment
    comment_pos=comment[ic].start_position[1]   #position on the line \start comment
    program_position=0                          #position in the c program
    line_counter=0                              #line counter in the c program
    position_on_counter=0                       #position on the line in the c program
    for c in codeCpp:
        if line_counter>=comment_line or (comment_pos>=comment_line and line_counter>=comment_line) : break
        program_position+=1
        position_on_counter+=1
        if c=='\n':
            line_counter+=1
            position_on_counter=0
    cleft=codeCpp[:program_position]
    cright=codeCpp[program_position:]
    if comment[ic].comment_text[:7]!='#pragma':
        codeCpp=cleft+" "+"//"+comment[ic].comment_text[1:]+cright
    else:
       codeCpp = cleft + " " + comment[ic].comment_text + f"{endline if line_counter ==0 and position_on_counter ==0 else ' '}" + cright  #FIXME '\n' in f string can be unsupported in some version of python
"""
#save on cpp file
with open(file_path_destination, "w") as file:
    file.write(codeCpp)

# compile to check sintax of the c++ code
subprocess.run(["g++", "-c", file_path_destination])
