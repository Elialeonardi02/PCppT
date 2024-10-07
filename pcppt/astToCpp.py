import ast

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
        self.classes={}     #{name classe[attributes, functions]
        self.functions={}   #functions {signature: body}
#parser
codeCpp = code()

class astToCppParser(ast.NodeVisitor):

    def __init__(self):
        self.indent_level = 0  #indent level
        self.current_function_name = None
        self.current_structure_name=None
        self.array_multitype_names=[]

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
        if class_name not in codeCpp.classes:
            codeCpp.classes[class_name]=[]
        else:
            raise
        #class_code = f"class {class_name} {{\n"
        self.indent_level += 1
        # Handle attributes and methods
        for body_node in node.body:
            class_code = self.visit(body_node)
            if isinstance(body_node, ast.AnnAssign):
                function_attribute_name=body_node.target.id
            elif isinstance(body_node, ast.FunctionDef):
                function_attribute_name = body_node.name
            else:           #FIXME handle the exception or others cases
                raise
            class_code+=' '*self.indent_level
            if isinstance(body_node, ast.AnnAssign) or isinstance(body_node, ast.FunctionDef):
                if len(function_attribute_name)>=2 and function_attribute_name[0]=='_' and function_attribute_name[1]!='_':
                    class_code += 'protected:'
                elif len(function_attribute_name)>=3 and function_attribute_name[0]=='_' and function_attribute_name[1]=='_':
                    class_code += 'private:'
                else:
                    class_code += 'public:'
            codeCpp.classes[class_name].append(class_code)
        self.indent_level -= 1
        self.current_structure_name=None

    def visit_FunctionDef(self, node):  #visit and translate to C++ FunctionDef node
        self.current_function_name=node.name #save name for check of recursive functions
        #type and nameof the function
        if node.returns is not None:
            function_type = node.returns.id #the type of the function is specified in the python source
        else:
            function_type = 'void'          #the type of the function is not specified in the python source #TODO use the template based on the type of parameters
        if self.current_structure_name is not None and (node.name=='__init__' or node.name==self.current_structure_name):   #is a constructor of a class
            signature = f"{self.indent()}{self.current_structure_name}("
        else:                                                                   #is a normal function
            signature = f"{self.indent()}{function_type} {node.name}("

        #parameters and types of the function
        for i in range(1 if self.current_structure_name is not None else 0, len(node.args.args)): #the i start from 1 when the fuction is declare in a class so as to remove the self keyword
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
            return signature+func_code
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

    #TODO list multitype is not working
    """
    def visit_List(self, node):
        #visit list with different types
        declaration='{'                 #TODO ad casting to the type of the union
        for index, elem in enumerate(node.elts):
            if type(elem.value)==int:
                value=elem.value
            elif type(elem.value)==str:
                value=f'"{elem.value}"'
            declaration+='{'+str(value)+'}'
            if index < len(node.elts) - 1:
                declaration += ', '
        declaration+='}'

        return declaration

    def visit_Subscript(self, node):    #visit and translate to C++ Subscript node (accessing elements) #FIXME add sintax for code outside of a function
        obj = self.visit(node.value)          #the object being indexed
        index = self.visit(node.slice)    #the index to access
        if obj in self.array_multitype_names:
            return f"(({obj}[{index}].getString()!=nullptr)? {obj}[{index}].getString() : {obj}[{index}].getInt())"
        else:
            return f"{obj}[{index}]"
    """

    def visit_Attribute(self, node):  # Visit and translate to C++ Attribute node
        if self.current_structure_name is None:
            value = self.visit(node.value)
        else:
            value='this'
        attr_name = node.attr

        return f"{value}{'->' if self.current_structure_name is not None else '.'}{attr_name}"

    def visit_targets(self, node):  # Visit and traslate to C++ targets elements. It is not a fuction of AST library
        targets = [self.visit(t) for t in node]
        return ', '.join(targets)

    def visit_Assign(self, node):   #visit and translate to C++ Assign node
        targets = self.visit_targets(node.targets) #left variable or variables
        if isinstance(node.value,ast.List):         #FIXME list multitype not work
            value=self.visit_List(node.value)
            assign_code = f"{self.indent()}{'typesArray '+targets[0]+'['+str(len(node.value.elts))+']'} = {value};\n"
            self.array_multitype_names.append(targets[0])
        else:
            value = self.visit(node.value)                  #operation
            assign_code=f"{self.indent()}{targets} = {value};\n"

        if self.current_function_name is None:  #assign is outside a function
            codeCpp.declarations+=assign_code
        else:                                   #assing is inside a function
            return assign_code

    def visit_AnnAssign(self, node): #visit and translate to C++ AnnAssign node(es. c:int=0)
        var_name = self.visit(node.target)      #name of the variable
        var_type = self.visit(node.annotation)  #type of the variable
        value = self.visit(node.value)          #value assign
        annAssign_code = f"{self.indent()}{var_type} {var_name}" + (f" = {'' if var_type in codeCpp.classes else ''} {value}" if value!='' else "") + ";\n" #assign with value and no value

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