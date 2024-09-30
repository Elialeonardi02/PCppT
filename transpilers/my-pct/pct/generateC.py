import ast


class ASTToCPlusPlus(ast.NodeVisitor):
    def __init__(self):
        self.indent_level = 0  # Controlla il livello di indentazione per ogni blocco di codice

    def visit_Module(self, node):
        """
        Visita il nodo Module che rappresenta il modulo principale.
        """
        code = ''
        for stmt in node.body:
            code += self.visit(stmt)  # Visita ogni statement nel corpo del modulo
        return code

    def visit_FunctionDef(self, node):
        """
        Visita il nodo FunctionDef per tradurre una funzione Python in una funzione C++.
        """
        # Determina il tipo di ritorno della funzione
        if node.returns is not None:
            function_type = node.returns.id  # Tipo di ritorno specificato nel codice Python
        else:
            function_type = 'void'  # Se non è specificato, usa 'void'

        # Costruisce l'intestazione della funzione
        func_code = f"{self.indent()}{function_type} {node.name}("

        # Traduci i parametri della funzione
        for i in range(len(node.args.args)):
            param_type = 'auto' if node.args.args[i].annotation is None else node.args.args[i].annotation.id
            param_name = node.args.args[i].arg
            func_code += f"{param_type} {param_name}"
            if i < len(node.args.args) - 1:
                func_code += ', '

        func_code += ') {\n'
        self.indent_level += 1

        # Traduci il corpo della funzione
        for stmt in node.body:
            func_code += self.visit(stmt)

        self.indent_level -= 1
        func_code += self.indent() + "}\n"

        return func_code

    def visit_If(self, node):
        condition = self.visit(node.test)
        if_code = f"{self.indent()}if ({condition}) {{\n"

        self.indent_level += 1
        for stmt in node.body:
            if_code += self.visit(stmt)
        self.indent_level -= 1
        if_code += self.indent() + "}\n"

        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                if_code += f"{self.indent()}else {self.visit(node.orelse[0])}"
            else:
                if_code += f"{self.indent()}else {{\n"
                self.indent_level += 1
                for stmt in node.orelse:
                    if_code += self.visit(stmt)
                self.indent_level -= 1
                if_code += self.indent() + "}\n"
        return if_code

    def visit_Return(self, node):
        return f"{self.indent()}return {self.visit(node.value)};\n"

    def visit_Assign(self, node):
        """
        Visita il nodo Assign per tradurre un'assegnazione in C++.
        """
        targets = [self.visit(t) for t in node.targets]
        value = self.visit(node.value)
        return f"{self.indent()}{' = '.join(targets)} = {value};\n"

    def visit_AugAssign(self, node):
        """
        Visita il nodo AugAssign per tradurre un'assegnazione incrementale in C++ (es: +=, %=).
        """
        target = self.visit(node.target)
        op = self.visit(node.op)
        value = self.visit(node.value)
        return f"{self.indent()}{target} {op}= {value};\n"

    def visit_BinOp(self, node):
        """
        Visita il nodo BinOp per tradurre un'operazione binaria in C++.
        """
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.visit(node.op)
        return f"{left} {op} {right}"

    # Operatori aritmetici
    def visit_Add(self, node):
        return "+"

    def visit_Sub(self, node):
        return "-"

    def visit_Mult(self, node):
        return "*"

    def visit_Div(self, node):
        return "/"

    def visit_Mod(self, node):
        return "%"

    def visit_Pow(self, node):
        return "**"

    def visit_FloorDiv(self, node):
        return "//"

    # Operatori logici
    def visit_BoolOp(self, node):
        op = self.visit(node.op)
        values = [self.visit(value) for value in node.values]
        return f" {op} ".join(values)

    def visit_And(self, node):
        return "&&"

    def visit_Or(self, node):
        return "||"

    # Operatori di confronto
    def visit_Compare(self, node):
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        operator = self.visit(node.ops[0])
        return f"{left} {operator} {right}"

    def visit_Eq(self, node):
        return "=="

    def visit_NotEq(self, node):
        return "!="

    def visit_Lt(self, node):
        return "<"

    def visit_LtE(self, node):
        return "<="

    def visit_Gt(self, node):
        return ">"

    def visit_GtE(self, node):
        return ">="

    def visit_Name(self, node):
        return node.id

    def visit_Num(self, node):
        return str(node.n)

    def indent(self):
        return "  " * self.indent_level

    def generic_visit(self, node):
        return ""


def generate_cpp_code_from_ast(python_ast):
    translator = ASTToCPlusPlus()
    return translator.visit(python_ast)
