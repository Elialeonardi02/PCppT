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
#print(ast.dump(fast, indent=4))
for i in range(0, len(comment)):
    print(comment[i])
c=generateC.generate_cpp_code_from_ast(fast)
print(c)