import ast

class ASTToCPlusPlus(ast.NodeVisitor):
    def __init__(self):
        self.indent_level = 0

    def visit_Module(self, node):
        code=''
        for stmt in node.body:
            code += self.visit(stmt)
        return code

    def visit_FunctionDef(self, node):
        # Assuming all functions return int for simplicity
        func_code = f"{self.indent()}int {node.name}("
        func_code += ", ".join([f"int {arg.arg}" for arg in node.args.args]) + ") {\n"
        self.indent_level += 1
        for stmt in node.body:
            func_code += self.visit(stmt)
        func_code += self.indent() + "}\n"
        self.indent_level -= 1
        return func_code

    def visit_Return(self, node):
        return f"{self.indent()}return {self.visit(node.value)};\n"

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.visit(node.op)
        return f"{left} {op} {right}"

    def visit_Add(self, node):
        return "+"

    def visit_Num(self, node):
        return str(node.n)

    def visit_Name(self, node):
        return node.id

    def indent(self):
        return "    " * self.indent_level

    def generic_visit(self, node):
        return ""

def generate_cpp_code_from_ast(python_ast):
    translator = ASTToCPlusPlus()
    return translator.visit(python_ast)