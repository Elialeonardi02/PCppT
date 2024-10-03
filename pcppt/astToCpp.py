import ast
from operator import truediv

from docutils.frontend import validate_encoding


#exceptionClasses
class UnsupportedCommandError(Exception):   #exception for unsupported command
    def __init__(self, command):
        super().__init__(f"Unsupported command: {command}")

class RecursiveFunctionError(Exception):    #exception for recursive functions
    def __init__(self, function_name):
        super().__init__(f"Recursive function not supported: {function_name}")

"""
class function():
    def __init__(self):
        self.signature=''
        self.body=''
"""
class code():
    def __init__(self):
        self.declarations=''
        self.functions={}   #functions {signature: body}
#parser
codeCpp = code()
class astToCppParser(ast.NodeVisitor):

    def __init__(self):
        self.indent_level = 0  #indent level
        self.current_function_name = None
        self.current_structure_name=None

    def visit_Module(self, node):   #visit the root of ast
        for astNode in node.body:       #visit all node of ast
            self.visit(astNode) #function from the ast import
        #return cppCode

    def indent(self):   #generate an indentation string based on the current level of indentation

        return "  " * self.indent_level

    def generic_visit(self, node):  #does nothing by default when visiting a node

        return ""

    def visit_Name(self, node): #visit and translate to C++ Name node

        return node.id

    def visit_Num(self, node):  #visit and translate to C++ Num node
        return str(node.n)

    def visit_Expr(self, node): # visit e translate in C++ Expr node
        return self.indent()+self.visit(node.value) + ";\n"

    def visit_ClassDef(self, node):  # visit e translate in C++ ClassDef node
        class_name = node.name
        self.current_structure_name = class_name
        class_code = f"class {class_name} {{\n"
        self.indent_level += 1

        constructor_code = f"{self.indent()}{class_name}() \n"  #class constructor

        # Handle attributes and methods
        for body_node in node.body:
            if isinstance(body_node, ast.FunctionDef): #body of constructor
                if body_node.name == '__init__':
                    constructor_code += self.visit(body_node)
                else:
                    method_code = self.visit(body_node)
                    class_code += method_code
            else:  # Gestisci le assegnazioni annotate
                class_code += self.visit(body_node)

        class_code += constructor_code

        self.indent_level -= 1
        class_code += "};\n"
        codeCpp.declarations += class_code
        self.current_structure_name=None

    def visit_FunctionDef(self, node):  #visit and translate to C++ FunctionDef node
        self.current_function_name=node.name #save name for check of recursive functions
        #type and nameof the function
        if node.returns is not None:
            function_type = node.returns.id #the type of the function is specified in the python source
        else:
            function_type = 'void'          #the type of the function is not specified in the python source #TODO use the template based on the type of parameters
        signature = f"{self.indent()}{function_type} {node.name}("

        #parameters and types of the function
        for i in range(len(node.args.args)):
            param_type = 'auto' if node.args.args[i].annotation is None else node.args.args[i].annotation.id #FIXME if the type is not specified raise an exception or type inference
            param_name = node.args.args[i].arg
            signature += f"{param_type} {param_name}"
            if i < len(node.args.args) - 1:
                signature += ', '
        signature += ')'

        self.indent_level += 1
        func_code='{\n'
        #body of the function
        for astNode in node.body:
            if not isinstance(astNode, ast.FunctionDef):    #the node is not a def of a function
                iBodyCode=self.visit(astNode)
                func_code += iBodyCode
            else:                                          #there is a function declaration in the body, add another signature and body in
                temp_indent_level=self.indent_level
                self.indent_level=0
                self.visit(astNode)
                self.indent_level=temp_indent_level

        self.indent_level -= 1
        func_code += self.indent() + "}\n"
        if self.current_structure_name is None:
            if signature not in codeCpp.functions:
                codeCpp.functions[signature] = ''
            else:
                raise UnsupportedCommandError(
                    f"{signature} is already defined")  # FIXME implements overloading operators
            codeCpp.functions[signature]=func_code
        else:
            return func_code
        self.current_function_name = None

    def visit_Call(self, node):  #visit and translate to C++ Call node(function call)
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

    def visit_For(self, node):  #visit and translate to C++ For node
        target = self.visit(node.target)    #counter
        iter_value = self.visit(node.iter)  #range
        loop_code = ""
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':   #range cicle
            if len(node.iter.args) == 1:  # range(stop)
                loop_code += f"{self.indent()}for (int {target} = 0; {target} < {self.visit(node.iter.args[0])}; ++{target}) {{\n"
            elif len(node.iter.args) == 2:  # range(start, stop)
                loop_code += f"{self.indent()}for (int {target} = {self.visit(node.iter.args[0])}; {target} < {self.visit(node.iter.args[1])}; ++{target}) {{\n"
            elif len(node.iter.args) == 3:  # range(start, stop, step)
                loop_code += f"{self.indent()}for (int {target} = {self.visit(node.iter.args[0])}; {target} < {self.visit(node.iter.args[1])}; {target} += {self.visit(node.iter.args[2])}) {{\n"
        else: #FIXME i have to handle the others type of for?
            raise UnsupportedCommandError(f"Unsupported iteration: {iter_value}")

        #corpo del ciclo
        self.indent_level += 1
        for astNode in node.body:
            loop_code += self.visit(astNode)

        self.indent_level -= 1
        loop_code += self.indent() + "}\n"

        return loop_code

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

    def visit_Attribute(self, node):  # Visit and translate to C++ Attribute node
        if self.current_structure_name is None:
            value = self.visit(node.value)
        else:
            value='this'
        attr_name = node.attr

        return f"{value}->{attr_name}"

    def visit_Assign(self, node):   #visit and translate to C++ Assign node
        targets = [self.visit(t) for t in node.targets] #left variable or variables
        value = self.visit(node.value)                  #operation

        assign_code=f"{self.indent()}{' = '.join(targets)} = {value};\n"

        if self.current_function_name is None:  #assign is outside a function
            codeCpp.declarations+=assign_code
        else:                                   #assing is inside a function
            return assign_code

    def visit_AnnAssign(self, node): #visit and translate to C++ AnnAssign node(es. c:int=0)
        var_name = self.visit(node.target)      #name of the variable
        var_type = self.visit(node.annotation)  #type of the variable
        value = self.visit(node.value)          #value assign
        print(value=='')
        annAssign_code = f"{self.indent()}{var_type} {var_name}" + (f" = {value}" if value!='' else "") + ";\n" #assign with value and no value
        if self.current_function_name is None and self.current_structure_name is None:  #annAssign is outside a function or class
            codeCpp.declarations+=annAssign_code
        else:                                   #annAssign is inside a function or class
            return annAssign_code

    def visit_AugAssign(self, node):    #visit and translate to C++ AugAssign node(es: i+=<value)
        target = self.visit(node.target)    #variable
        op = self.visit(node.op)            #operator
        value = self.visit(node.value)      #value

        augAssign_code=f"{self.indent()}{target} {op}= {value};\n"
        if self.current_function_name is None:  #augAssign is outside a function
            codeCpp.declarations+=augAssign_code
        else:
            return augAssign_code               #augAssign is inside a function

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
    try:
        astToCppParser().visit(python_ast)
        return codeCpp
    except (UnsupportedCommandError, RecursiveFunctionError) as e:
        raise