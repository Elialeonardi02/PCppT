import ast

from executing.executing import function_node_types


class ASTToCPlusPlus(ast.NodeVisitor):
    def __init__(self):
        self.indent_level = 0

    def visit_Module(self, node):
        code=''
        for stmt in node.body:
            code += self.visit(stmt)
        return code

    def visit_FunctionDef(self, node):
        #set type of fuction
        if node.returns is not None:
            function_type=node.returns.id #fuction type spefified in the python code
        else:
            function_type='void'    #function type not specified in the python code
        func_code = f"{self.indent()}{function_type} {node.name}(" #node.returns is null: the type of the function is not defined in the python, else the type of the function of the function is defined in the python
        #set parameters
        for i in range(0, len(node.args.args)):
            func_code += f"{'auto' if node.args.args[i].annotation is None else node.args.args[i].annotation.id} {node.args.args[i].arg}{',' if i+1<len(node.args.args) else ''}"
        func_code +='){\n'
        self.indent_level += 1
        for stmt in node.body:
            func_code += self.visit(stmt)
        func_code += self.indent() + "}\n"
        self.indent_level -= 1
        return func_code

    def visit_For(self, node):
        # Ottieni la variabile di iterazione (il target del for loop)
        target = self.visit(node.target)
        # Controlla se stiamo iterando su un range (caso comune in Python)
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":
            range_args = [self.visit(arg) for arg in node.iter.args]  # Gestisci gli argomenti di range
            if len(range_args) == 1:
                # Sintassi del tipo: for (int i = 0; i < range_arg[0]; ++i)
                iter_code = f"for (int {target} = 0; {target} < {range_args[0]}; {target}++)"
            elif len(range_args) == 2:
                # Sintassi con inizio e fine: for (int i = range_arg[0]; i < range_arg[1]; ++i)
                iter_code = f"for (int {target} = {range_args[0]}; {target} < {range_args[1]}; {target}++)"
            elif len(range_args) == 3:
                # Sintassi con inizio, fine e step: for (int i = range_arg[0]; i < range_arg[1]; i += range_arg[2])
                iter_code = f"for (int {target} = {range_args[0]}; {target} < {range_args[1]}; {target} += {range_args[2]})"
        else:
            # Caso generale, iterazione su collezioni (C++ richiede iteratore qui, Python usa direttamente l'oggetto)
            iter_code = f"for (auto {target} : {self.visit(node.iter)})"

        # Aggiungi il corpo del ciclo
        loop_code = iter_code + " {\n"
        self.indent_level += 1
        for stmt in node.body:
            loop_code += self.visit(stmt)
        self.indent_level -= 1
        loop_code += self.indent() + "}\n"

        return loop_code

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