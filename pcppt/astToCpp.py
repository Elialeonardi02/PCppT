import ast

import typesMapping as tm
import exceptions as ex

class code():
    def __init__(self):
        self.globalCode=''  #code in the global scope
        self.classes={}     #{name classe[{signature: body},attributes]
        self.functions={}   #functions {signature: body}
codeCpp = code()

#class parse python Ast to c++ code
class astToCppParser(ast.NodeVisitor):

    def __init__(self): #constructor
        self.indent_level = 0               #indent level of cpp code
        self.current_function_name = None   #function signature of the node being explored, if is a FunctionDef node
        self.current_structure_name = None  #name of the class in the node being explored, if is a ClassDef node
        #self.array_multitype_names=[]

    def visit_Module(self, node):   #visit the root node of the AST
        for astNode in node.body:       #iterate through all the child nodes in the module body
            self.visit(astNode)          #visit each node

    def indent(self):   #generate an indentation string of space based on the current level of indentation to formate the code

        return "  " * self.indent_level

    def generic_visit(self, node):  #Called if no explicit visitor function exists for a node.
        #FIXME raise an exception when threre is not a function to explore the Node?
        return ""

    def visit_Name(self, node): #visit and translate to C++ Name node

        return node.id

    def visit_Num(self, node):  #visit and translate to C++ Num node

        return str(node.n)

    def visit_Expr(self, node): # visit e translate in C++ Expr node

        return self.indent()+self.visit(node.value) + ";\n"

    def visit_ClassDef(self, node):  # visit e translate in C++ ClassDef node
        class_name = node.name
        self.current_structure_name = class_name                                                                        #save name of class for codeCpp.classes dictionary and scope dictionary

        #check the class is already defined
        if class_name not in codeCpp.classes:                                                                           #the class isn't already defined
            codeCpp.classes[class_name]=[{}]                                                                                #the first element of codeCpp.classes is {signature:body} of  functions
        else:                                                                                                           #the class is already defined
            raise ex.AlreadyDefinedError(class_name)
        self.indent_level += 1

        #parse attributes and methods
        for body_node in node.body:
            if isinstance(body_node, ast.AnnAssign):                                                                        #body_node is an attribute
                function_attribute_name=body_node.target.id                                                                     #save name attribute
            elif isinstance(body_node, ast.FunctionDef):                                                                    #body_node is a method
                function_attribute_name = body_node.name                                                                        #save name method
            else:                                                                                                           #body_node is unsopported in class body
                raise ex.UnsupportedCommandError(node.body)

            body_node_code=self.indent()
            #visibility of fuction or attribute
            #if isinstance(body_node, ast.AnnAssign) or isinstance(body_node, ast.FunctionDef):      #FIXME this if is necessary?
            if len(function_attribute_name)>=2 and function_attribute_name[0]=='_' and function_attribute_name[1]!='_':     #_<name> protected
                body_node_code += 'protected:'
            elif len(function_attribute_name)>=3 and function_attribute_name[0]=='_' and function_attribute_name[1]=='_':   #__<name> private
                body_node_code += 'private:'
            elif function_attribute_name is not None:                                                                       #<name> public
                body_node_code += 'public:'

            #add code to codeCpp
            if isinstance(body_node, ast.AnnAssign):                                                                        #is attribute
                body_node_code += self.visit(body_node)
                codeCpp.classes[class_name].append(body_node_code)                                                              #add code attribute to class list
            elif isinstance(body_node, ast.FunctionDef):                                                                    #is a method
                signature,method_body = self.visit(body_node)
                signature=body_node_code+signature                                                                              #add visibility to signature
                if signature not in codeCpp.classes[class_name][0]:                                                             #the method is not arleady defined
                    codeCpp.classes[class_name][0][signature]=f"\n{self.indent()}{method_body}"
                else:                                                                                                           #the method is arleady defined
                    raise ex.AlreadyDefinedError(f"in this class {signature}")

        #end of ClassDef node explorations
        self.indent_level -= 1
        self.current_structure_name=None

    def visit_FunctionDef(self, node):  #visit and translate to C++ FunctionDef node
        self.current_function_name=node.name                                                                                                #save name for checking of recursive functions

        #determine the function's type and name
        if node.returns is not None:                                                                                                        #type specified in Python source
            function_type = tm.pythonTypes_CppTypes.get(str(node.returns.id))                                                                   #use typesMapping to traslate python type to c++ type
        else:                                                                                                                               #type of function is not specified in the python source
            function_type = 'template <typename T> T'                                                                                           #use template in c++
        if (self.current_structure_name is not None and                                                                                     #previos node is not a class
                (node.name=='__init__' or node.name==self.current_structure_name)):                                                         #is a constructor of a class
            signature = f"{self.indent()}{self.current_structure_name}("                                                                        #signature construction
        else:                                                                                                                               #is a normal function or a method of a class
            signature = f"{self.indent()}{function_type} {node.name}("                                                                          #normal signature with type

        #parameters and types of the function
        for i in range(1 if self.current_structure_name is not None else 0, len(node.args.args)):                                           #start from 1 for methods to skip 'self'
            param_type = 'auto' if node.args.args[i].annotation is None else tm.pythonTypes_CppTypes.get(str(node.args.args[i].annotation.id))  #use 'auto' if type not specified #FIXME if the type is not specified raise an exception, type inference or use auto with vitis
            param_name = node.args.args[i].arg
            signature += f"{param_type} {param_name}"
            if i < len(node.args.args) - 1:                                                                                                 #it is not last parameter
                signature += ', '
        signature += ')'
        self.current_function_name = signature                                                                                              #save name for checking of recursive functions and scope

        #add parameters to scope of the function in typesMapping.scope
        for i in range(1 if self.current_structure_name is not None else 0, len(node.args.args)):                                           #start from 1 for methods to skip 'self'
            param_type = 'auto' if node.args.args[i].annotation is None else tm.pythonTypes_CppTypes.get(str(node.args.args[i].annotation.id))  #use 'auto' if type not specified #FIXME if the type is not specified raise an exception, type inference or use auto with vitis
            param_name = node.args.args[i].arg
            tm.add_to_scope(self.current_function_name,self.current_structure_name,param_name,param_type)

        self.indent_level += 1

        # body of the function
        func_code='{\n'
        for astNode in node.body:
            if not isinstance(astNode, ast.FunctionDef):                                                                                        #the node is not a def of a function
                iBodyCode=self.visit(astNode)
                func_code += iBodyCode
            else:                                                                                                                               #a function declaration in the body
                temp_indent_level=self.indent_level
                self.indent_level=0
                self.visit(astNode)
                self.indent_level=temp_indent_level
                self.current_function_name = signature                                                                                          #reset current_function_name to current signature after visit

        self.indent_level -= 1
        func_code += self.indent() + "}\n"

        #save signature and func_code in codeCpp
        if self.current_structure_name is None:                                                                                                 #is a function
            if signature not in codeCpp.functions:                                                                                                  #function is not already defined
                codeCpp.functions[signature] = ''
            else:                                                                                                                                   #function is already defined
                raise ex.AlreadyDefinedError(signature)
            codeCpp.functions[signature]=func_code
        else:                                                                                                                                   #is a method of a class
            return signature, func_code

        #end of functionDef node explorations
        self.current_function_name = None

    def visit_Call(self, node):  #visit and translate to C++ Call node(function call)
        #recursive function check
        function_name = self.visit(node.func)                       #get the name of the function being called
        if function_name==self.current_function_name:               #is recursive function
            raise ex.RecursiveFunctionError(function_name)

        #check if the function is supported
        if (function_name not in codeCpp.classes and                #the fuction is not in the code.class
                function_name not in codeCpp.functions and          #the fuction in not in the code.functions
                function_name not in tm.pythonFunction_toParse):    #the function is not in the list of parsable Python functions
            raise RuntimeError(f"Function or class' {function_name}' is not supported.")

        #parameters of the call
        args = [self.visit(arg) for arg in node.args]

        return f"{function_name}({', '.join(args)})"

    def visit_For(self, node):  #visit and translate to C++ For node
        target = self.visit(node.target)                                                                                #loop counter
        iter_value = self.visit(node.iter)                                                                              #iterator (range)
        loop_code = ""

        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':   #range cicle
            if len(node.iter.args) == 1:                                                                                    #range(stop) #FIXME add type inference for the target?
                loop_code += f"{self.indent()}for (int {target} = 0; {target} < {self.visit(node.iter.args[0])}; ++{target}) {{\n"
            elif len(node.iter.args) == 2:                                                                                  #range(start, stop)
                loop_code += f"{self.indent()}for (int {target} = {self.visit(node.iter.args[0])}; {target} < {self.visit(node.iter.args[1])}; ++{target}) {{\n"
            elif len(node.iter.args) == 3:                                                                                  #range(start, stop, step)
                loop_code += f"{self.indent()}for (int {target} = {self.visit(node.iter.args[0])}; {target} < {self.visit(node.iter.args[1])}; {target} += {self.visit(node.iter.args[2])}) {{\n"
        else: #FIXME i have to handle the others type of for?
            raise ex.UnsupportedCommandError(f"{iter_value} unsupported iterator")

        #loop body
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

    #FIXME list multitype is NOT  WORK
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

    def visit_Attribute(self, node):  #visit and translate to C++ Attribute node
        if self.current_structure_name is None:
            value = self.visit(node.value)
        else:
            value='this'
        attr_name = node.attr

        return f"{value}{'->' if self.current_structure_name is not None else '.'}{attr_name}"

    def visit_targets(self, node):  #visit and traslate to C++ targets elements. It is not a fuction of AST library
        targets = [self.visit(t) for t in node]

        return ', '.join(targets)

    def visit_Assign(self, node):   #visit and translate to C++ Assign node
        targets = self.visit_targets(node.targets)                                                                                  #left variable or variables
        """
        if isinstance(node.value,ast.List):         #FIXME list multitype NOT WORK
            value=self.visit_List(node.value)
            assign_code = f"{self.indent()}{'typesArray '+targets[0]+'['+str(len(node.value.elts))+']'} = {value};\n"
            self.array_multitype_names.append(targets[0])
        else: """
        value = self.visit(node.value)
        assign_code=''
        type=f"{self.indent()}{tm.check_scope(self.current_function_name,self.current_structure_name,targets,node.value.value)}";   #generate type for variable if it is not defined
        for target in targets:                                                                                                      #different instruction for every target
            assign_code+=f"{type}{target} = {value};\n"

        if self.current_function_name is None:                                                                                      #assign is outside a function,method,class
            if(targets not in tm.pythonTypes_CppTypes):
                codeCpp.globalCode+=assign_code
        else:                                                                                                                       #assing is inside a function,method,class
            return assign_code

    def visit_AnnAssign(self, node): #visit and translate to C++ AnnAssign node(es. c:int=0 or c:int;)
        #generate assign code
        var_name = self.visit(node.target)                                                                                                                  #name variable
        var_type = tm.pythonTypes_CppTypes.get(self.visit(node.annotation))                                                                                 #type variable
        value = self.visit(node.value)                                                                                                                      #value assign
        annAssign_code = f"{self.indent()}{var_type} {var_name}" + (f" = {'' if var_type in codeCpp.classes else ''} {value}" if value!='' else "") + ";\n" #assign with value and no value

        #add variable to typesMapping.scope
        tm.add_to_scope(self.current_function_name,self.current_structure_name,var_name,var_type)

        if self.current_function_name is None and self.current_structure_name is None:                                                                      #annAssign is outside a function or class
            codeCpp.globalCode+=annAssign_code
        else:                                                                                                                                               #annAssign is inside a function or class
            return annAssign_code

    def visit_AugAssign(self, node):    #visit and translate to C++ AugAssign node(es: i+=<value)
        target = self.visit(node.target)        #variable
        op = self.visit(node.op)                #operator
        value = self.visit(node.value)          #value

        augAssign_code=f"{self.indent()}{target} {op}= {value};\n"
        if self.current_function_name is None:  #augAssign is outside a function
            codeCpp.globalCode+=augAssign_code
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
    def visit_Add(self, node):  #visit and translate to C++ Add node

        return "+"

    def visit_Sub(self, node):  #visit and translate to C++ Sub node

        return "-"

    def visit_Mult(self, node): #visit and translate to C++ Mult node

        return "*"

    def visit_Div(self, node):  #visit and translate to C++ Div node

        return "/"

    def visit_Mod(self, node):  #visit and translate to C++ Mod node

        return "%"

    def visit_Pow(self, node):  #visit and translate to C++ Pow node

        return "**"

    def visit_FloorDiv(self, node): #visit and translate to C++ FloorDiv node

        return "//"

    #boolean operators
    def visit_And(self, node):  #visit and translate to C++ And node

          return "&&"

    def visit_Or(self, node):   #visit and translate to C++ Or node

        return "||"

    #comparison operator
    def visit_Eq(self, node):   #visit and translate to C++ Eq node

        return "=="

    def visit_NotEq(self, node):    #visit and translate to C++ NotEq node

        return "!="

    def visit_Lt(self, node):   #visit and translate to C++ Lt node

        return "<"

    def visit_LtE(self, node):  #visit and translate to C++ Lte node

        return "<="

    def visit_Gt(self, node): #visit and translate to C++ Gt Node

        return ">"

    def visit_GtE(self, node):  #visit and translate to C++ Gte node

        return ">="

def generateAstToCppCode(python_ast):
    try:
        astToCppParser().visit(python_ast)
        print(tm.scope) #TODO remove, use for debugging
        return codeCpp
    except (ex.UnsupportedCommandError, ex.RecursiveFunctionError) as e:
        raise