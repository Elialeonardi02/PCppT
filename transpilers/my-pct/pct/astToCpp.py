import ast

class UnsupportedCommandError(Exception):
    def __init__(self, command):
        super().__init__(f"Unsupported command: {command}")

class RecursiveFunctionError(Exception):    #exception for recursive functions
    def __init__(self, function_name):
        super().__init__(f"Recursive function not supported: {function_name}")
        
class astToCppParser(ast.NodeVisitor):
    def __init__(self):
        self.indent_level = 0  #indent level
        self.current_function_name = None

    def visit_Module(self, node):   #visit the root of ast
        code = ''                       #c code
        for astNode in node.body:       #visit all node of ast
            code += self.visit(astNode) #function from the ast import

        return code

    def indent(self):   #generate an indentation string based on the current level of indentation

        return "  " * self.indent_level

    def generic_visit(self, node):  #does nothing by default when visiting a node

        return ""

    def visit_Name(self, node): #visit and translate to C++ Name node

        return node.id

    def visit_Num(self, node):  #visit and translate to C++ Num node

        return str(node.n)

    def visit_Expr(self, node): # visita e traduce in C++ Expr node
        return self.indent()+self.visit(node.value) + ";\n"  # visitiamo il valore dell'espressione e aggiungiamo il punto e virgola

    def visit_FunctionDef(self, node):  #visit and translate to C++ FunctionDef node
        self.current_function_name=node.name #save name for check of recursive functions

        #type and nameof the function
        if node.returns is not None:
            function_type = node.returns.id #the type of the function is specified in the python source
        else:
            function_type = 'void'          #the type of the function is not specified in the python source #TODO use the template based on the type of parameters
        func_code = f"{self.indent()}{function_type} {node.name}("

        #parameters and types of the function
        for i in range(len(node.args.args)):
            param_type = 'auto' if node.args.args[i].annotation is None else node.args.args[i].annotation.id
            param_name = node.args.args[i].arg
            func_code += f"{param_type} {param_name}"
            if i < len(node.args.args) - 1:
                func_code += ', '
        func_code += ') {\n'
        self.indent_level += 1

        #body of the function
        for astNode in node.body:
            func_code += self.visit(astNode)
        self.indent_level -= 1
        func_code += self.indent() + "}\n"

        self.current_function_name=None

        return func_code

    def visit_Call(self, node):  # visit and translate to C++ Call node(function call)
        #recursive function check
        function_name = self.visit(node.func)  # Get the name of the function being called
        if function_name==self.current_function_name:
            raise RecursiveFunctionError(function_name)
        # Check if the function is supported (you can customize this list)
        unsupported_functions = {'print', 'input', 'len'}  # Example of unsupported functions
        if function_name in unsupported_functions:
            raise RuntimeError(f"Function '{function_name}' is not supported.")

        # Handle function arguments
        args = [self.visit(arg) for arg in node.args]
        return f"{function_name}({', '.join(args)})"

    def visit_If(self, node):   #visit and translate to C++ If node
        #if condition
        condition = self.visit(node.test)
        if_code = f"{self.indent()}if ({condition}) {{\n"

        #if body
        self.indent_level += 1
        for astNode in node.body:
            if_code += self.visit(astNode)
        self.indent_level -= 1
        if_code += self.indent() + "}\n"

        #else
        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):    #elseif
                if_code += f"{self.indent()}else {self.visit(node.orelse[0])}"
            else:                                                               #normal else
                if_code += f"{self.indent()}else {{\n"
                self.indent_level += 1
                for astNode in node.orelse:
                    if_code += self.visit(astNode)
                self.indent_level -= 1
                if_code += self.indent() + "}\n"

        return if_code

    def visit_Return(self, node):   #visit and translate to C++ Return node

        return f"{self.indent()}return {self.visit(node.value)};\n"

    def visit_Assign(self, node):   #visit and translate to C++ Assign node
        targets = [self.visit(t) for t in node.targets] #left variable or variables
        value = self.visit(node.value)                  #operation

        return f"{self.indent()}{' = '.join(targets)} = {value};\n"

    def visit_AugAssign(self, node):    #visit and translate to C++ AugAssign node(es: i+=<value)
        target = self.visit(node.target)    #variable
        op = self.visit(node.op)            #operator
        value = self.visit(node.value)      #value

        return f"{self.indent()}{target} {op}= {value};\n"

    def visit_BinOp(self, node):    #visit and translate to C++ BinOp node
        left = self.visit(node.left)    #left member
        right = self.visit(node.right)  #right member
        op = self.visit(node.op)        #operator

        return f"{left} {op} {right}"

    def visit_BoolOp(self, node):   #visit and translate to C++ BoolOp node
        op = self.visit(node.op)                                #operator
        values = [self.visit(value) for value in node.values]   #values

        return f" {op} ".join(values)

    def visit_Compare(self, node):  #visit and translate to C++ Compare node
        left = self.visit(node.left)            #left element to compare
        right = self.visit(node.comparators[0]) #right element to compare
        op = self.visit(node.ops[0])            #operator

        return f"{left} {op} {right}"

    #aritmetics operators
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

    #boolean operators
    def visit_And(self, node):
          return "&&"

    def visit_Or(self, node):
        return "||"

    #comparison operator
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

def generateAstToCppCode(python_ast):
    #try:
        translator = astToCppParser()
        return translator.visit(python_ast)
    #except (UnsupportedCommandError, RecursiveFunctionError) as e:
        #print(e)