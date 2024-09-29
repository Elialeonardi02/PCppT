import generateC
import generateAST
import sys
import ast

if len(sys.argv) != 2:
    print("Usage: python your_script.py <path_to_python_file>")
    sys.exit(1)

file_path = sys.argv[1]

fast, comment = generateAST.generate_commented_ast(file_path)

print("Commented AST:")
print(ast.dump(fast, indent=4))

code=generateC.generate_cpp_code_from_ast(fast)
for ic in range(0, len(comment)):
    comment_line=comment[ic].start_position[0]
    comment_pos=comment[ic].start_position[1]
    program_position=0
    line_counter=0
    position_on_counter=0
    for c in code:
        if line_counter>=comment_line or (comment_pos>=comment_line and line_counter>=comment_line) : break
        program_position+=1
        position_on_counter+=1
        if c=='\n':
            line_counter+=1
            position_on_counter=0
    cleft=code[:program_position-1]
    cright=code[program_position-1:]
    if comment[ic].comment_text[:7]!='#pragma':
        code=cleft+" "+"//"+comment[ic].comment_text[1:]+f"{'\n'if line_counter==0 and position_on_counter==0 else ' '}"+cright
    else:
        code = cleft + " " + comment[ic].comment_text + f"{'\n' if line_counter ==0 and position_on_counter ==0 else ' '}" + cright
print(code)