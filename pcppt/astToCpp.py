import ast
from inspect import signature

import typesMapping as tm
import exceptions as ex
import codeCpp.codeCppClass as cppc


class astToCppParser(ast.NodeVisitor):

    def __init__(self): #constructor
        self.indent_level = 0                       #indent level of cpp code
        self.current_structure_name = None          #contain name of the exploring ClassDef node,
        self.current_function_name = None           #contain name of the exploring FunctionDef node,use for check recursive function
        self.current_function_signature=None        #contain function signature of the exploring FunctionDef Node, use for scope check

        # flag array single type
        self.array_single_type_declaration = False  # true: value node to explore in annAssignNode is a list, use for declaration of array single type


    def visit_Module(self, node):   #visit the root node of the AST
        for astNode in node.body:       #iterate through all the child nodes in the module body
            self.visit(astNode)         #visit each node

    def indent(self):   #generate an indentation string of space based on the current level of indentation to formate the code

        return "  " * self.indent_level

    def generic_visit(self, node):  #Called if no explicit visitor function exists for a node.

        return ""

    def visit_Name(self, node): #visit and translate to C++ Name node

        return node.id

    def visit_Num(self, node):  #visit and translate to C++ Num node

        return str(node.n)

    def visit_Constant(self, node):  #visit and translate to C++ Constant node
        if isinstance(node.value, str): #parse for string declaration
            return f"\"{node.value}\""

        return node.value

    def visit_Expr(self, node): # visit e translate in C++ Expr node

        return self.indent()+self.visit(node.value) + ";\n"

    def visit_ClassDef(self, node):  # visit e translate in C++ ClassDef node
        self.current_structure_name = node.name #save name of class for cppc.classes dictionary and scope

        #check class is already defined
        if self.current_structure_name not in cppc.cppCodeObject.classes:   #class isn't already define
            cppc.cppCodeObject.classes[self.current_structure_name]=[{}]        #add class to scope
        else:                                                               #class already define
            raise ex.AlreadyDefinedError(self.current_structure_name)
        self.indent_level += 1

        #parse attributes and methods
        for body_node in node.body:
            if isinstance(body_node, ast.AnnAssign):    #body_node is an attribute
                function_attribute_name=body_node.target.id #save name attribute
            elif isinstance(body_node, ast.FunctionDef):    #body_node is a method
                function_attribute_name = body_node.name    #save name method
            else:                                       #body_node is unsopported in class body
                raise ex.UnsupportedCommandError(node.body)
            body_node_code=self.indent()    #cpp code of body_node

            #visibility of function or attribute
            if len(function_attribute_name)>=2 and function_attribute_name[0]=='_' and function_attribute_name[1]!='_': #_<name> -> protected
                body_node_code += 'protected:'
            elif len(function_attribute_name)>=3 and function_attribute_name[0]=='_' and function_attribute_name[1]=='_'\
                    and function_attribute_name[-2:]!='__': #__<name> -> private
                body_node_code += 'private:'
            elif function_attribute_name is not None:   #<name> -> public
                body_node_code += 'public:'

            #add code to cppc.cppCodeObject[self.current_structure_name
            if isinstance(body_node, ast.AnnAssign):    #is attribute
                body_node_code += self.visit(body_node)
                cppc.cppCodeObject.classes[self.current_structure_name].append(body_node_code)
            elif isinstance(body_node, ast.FunctionDef):    #is a method
                signature,method_body = self.visit(body_node)
                signature=body_node_code+signature                 #add visibility to signature
                if signature not in cppc.cppCodeObject.classes[self.current_structure_name][0]:#the method is not arleady defined
                    cppc.cppCodeObject.classes[self.current_structure_name][0][signature]=f"\n{self.indent()}{method_body}"
                else:                                              #the method is arleady defined
                    raise ex.AlreadyDefinedError(f"in this class {signature}")


        #end of ClassDef node explorations
        self.indent_level -= 1
        self.current_structure_name=None

    def visit_FunctionDef(self, node):  #visit and translate to C++ FunctionDef node
        # save name for checking of recursive functions
        self.current_function_name = node.name

        #determine function type and name
        if node.returns is not None:    #type specified in Python source
            function_type = tm.pythonTypes_CppTypes.get(str(self.visit_returns(node.returns)))  #use typesMapping to traslate python type to c++ type
        else:   #type of function is not specified in the python source
            function_type = 'template <typename T> T'   #use template in c++
        if (self.current_structure_name is not None and #outside node is not a class
                (node.name=='__init__' or node.name==self.current_structure_name)): #function is a constructor of a class
            signature = f"{self.current_structure_name}("    #signature construction
        else:   #is a normal function or a method of a class
            signature = f"{function_type} {node.name}(" #normal signature with type

        tm.add_to_callableFunction(self.current_structure_name, self.current_function_name, node.name)
        #parameters and types of the function
        for i in range(1 if self.current_structure_name is not None else 0, len(node.args.args)):   #start from 1 for methods to skip 'self'
            param_type = 'auto' if node.args.args[i].annotation is None else tm.pythonTypes_CppTypes.get(str(node.args.args[i].annotation.id))  #use 'auto' if type not specified #FIXME if the type is not specified raise an exception, type inference or use auto with vitis
            param_name = node.args.args[i].arg
            signature += f"{param_type} {param_name}"
            if i < len(node.args.args) - 1: #it is not last parameter
                signature += ', '
        signature += ')'

        #add parameters to scope of the function in typesMapping.scope
        self.current_function_signature = signature
        signature=self.indent()+signature

        for i in range(0, len(node.args.args)):                                           #start from 1 for methods to skip 'self'
            param_type = 'auto' if node.args.args[i].annotation is None else tm.pythonTypes_CppTypes.get(str(node.args.args[i].annotation.id))  #use 'auto' if type not specified #FIXME if the type is not specified raise an exception, type inference or use auto with vitis
            param_name = node.args.args[i].arg
            if param_name=='self': #i==1
                tm.add_to_scope(self.current_function_signature,self.current_structure_name)
            else:
                tm.add_to_scope(self.current_function_signature, self.current_structure_name,param_name,param_type)

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
                self.current_function_name = node.name                                                                                          #reset current_function_name to current signature after visit
                self.current_function_signature = signature

        self.indent_level -= 1
        func_code += self.indent() + "}\n"


        #save signature and func_code in cppc
        if self.current_structure_name is None:                                                                                                 #is a function
            if signature not in cppc.cppCodeObject.functions:                                                                                                  #function is not already defined
                cppc.cppCodeObject.functions[signature] = ''
            else:   #FIXME it is the same control of tm.add_to_scope                                                                                                                              #function is already defined
                raise ex.AlreadyDefinedError(signature)
            cppc.cppCodeObject.functions[signature]=func_code
        else:                                                                                                                                   #is a method of a class
            return signature, func_code


        #end of functionDef node explorations
        self.current_function_name = None
        self.current_function_signature = None

    def visit_Lambda(self, node):
        # parameters and types of the function
        signature="("
        for i, arg in enumerate(node.args.args):
            signature += f"auto {arg.arg}"
            if i < len(node.args.args) - 1:  # Aggiunge una virgola se non è l'ultimo parametro
                signature += ', '
        signature += ")"
        return  f"[]{signature} {{return {self.visit(node.body)};}}",signature

    def visit_Call(self, node):  #visit and translate to C++ Call node(function call)
        #recursive function check
        function_name= self.visit(node.func)    #get the name of the function being called
        if function_name==self.current_function_name:   #is recursive function
            raise ex.RecursiveFunctionError(function_name)

        #check if the function is supported
        if not tm.check_callableFunction(self.current_structure_name, self.current_function_name, function_name): #FIXME check of method call on instance doesn't work
            raise ex.NotCallableError(function_name)

        #parameters of the call
        args = [str(self.visit(arg)) for arg in node.args]

        return f"{function_name}({', '.join(args)})"

    def visit_For(self, node):  #visit and translate to C++ For node
        target = self.visit(node.target)    #loop counter
        iter_values = []
        #target type_inference #TODO add more type
        types=[]
        type_target=None
        for arg in node.iter.args:
            iter_values.append(self.visit(arg))
            if not isinstance(arg,ast.Name):
                types.append(type(self.visit(arg)))
        if len(types)==2:
            if types[0]==types[1]:
                type_target =types[0].__name__
            elif {types[0], types[1]}.issubset({int, float}):
                type_target='float'
        else:
            type_target=types[0]
        type_target=tm.pythonTypes_CppTypes.get(type_target)
        loop_code = self.indent()
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':   #range cicle
            if len(iter_values) == 1:                                                                                    #range(stop)
                loop_code += f"for ({type_target} {target} = 0; {target} < {iter_values[0]}; ++{target}) {{\n"
            elif len(iter_values) == 2:                                                                                  #range(start, stop)
                loop_code += f"for ({type_target} {target} = {iter_values[0]}; {target} < {iter_values[1]}; ++{target}) {{\n"
            elif len(iter_values) == 3:                                                                                  #range(start, stop, step)
                loop_code += f"for ({type_target} {target} = {iter_values[0]}; {target} < {iter_values[1]}; {target} += {iter_values[2]}) {{\n"
        else: #FIXME i have to handle the others type of for?
            raise ex.UnsupportedCommandError(f"{iter_values} unsupported iterator")

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
            if_code += str(self.visit(astNode))
        self.indent_level -= 1
        if_code += self.indent() + "}\n"

        #else
        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):    #elseif
                if_code += f"{self.indent()}else {self.visit(node.orelse[0])}"
            else:   #normal else
                if_code += f"{self.indent()}else {{\n"
                self.indent_level += 1
                for astNode in node.orelse:
                    if_code += str(self.visit(astNode))
                self.indent_level -= 1
                if_code += self.indent() + "}\n"

        self.is_in_if=False

        return if_code

    def visit_Return(self, node):   #visit and translate to C++ Return node

        return f"{self.indent()}return {self.visit(node.value)};\n"

    def visit_returns(self, node):  #part of Return node
        if isinstance(node, ast.Name):
            return self.visit_Name(node)
        elif isinstance(node, ast.Constant):
            return str(self.visit_Constant(node))

    def visit_List(self, node):
        if self.array_single_type_declaration:    #is type of array one type element declaration
            return tm.corret_value(self.visit(node.elts[0]))
        else:
            elements = [f"{tm.corret_value(self.visit(el))}" for el in node.elts]
            return f"{', '.join(elements)}"

    def visit_Dict(self, node):
        dictionary={}
        for k,v in zip(node.keys,node.values):
            dictionary[self.visit(k)]=self.visit(v)
        return dictionary

    def visit_Subscript(self, node):    #visit and translate to C++ Subscript node (accessing elements) #FIXME add sintax for code outside of a function
        obj = self.visit(node.value)          #the object being indexed
        index = self.visit(node.slice)    #the index to access
        type=tm.get_var_type_scope(self.current_function_signature,self.current_structure_name,obj)
        if type in tm.pythonTypes_CppTypesArrays:
            return f"{obj}[{index}]"
        else:   #FIXME is it necessary without flextype and dict?
            return [f"{self.visit(node.value)}[{self.visit(node.slice)}]"]

    def visit_Attribute(self, node):  #visit and translate to C++ Attribute node
        if self.current_structure_name is None:
            value = self.visit(node.value)
        else:
            value='this'
        attr_name = node.attr
        return f"{value}{'->' if self.current_structure_name is not None else '.'}{attr_name}"  #FIXME not correct if use instance of other class

    def visit_targets(self, node):  #visit and traslate to C++ targets elements. It is not a fuction of AST library
        targets=[]
        if isinstance(node[0], ast.Tuple):
             for el in node[0].elts:
                 targets.append(el.id)
        elif isinstance(node[0],ast.Attribute):
            return[node[0].attr]
        elif isinstance(node[0],ast.Name):
            for el in node:
                targets.append(el.id)
        elif isinstance(node[0],ast.Subscript):
            return [self.visit(node[0])]
        return targets

    def visit_Assign(self, node):   #visit and translate to C++ Assign node
        targets= self.visit_targets(node.targets)#left variable or variables
        value = self.visit(node.value)
        assign_code = self.indent()
        for target in targets:
            if isinstance(node.targets[0],ast.Attribute) and self.current_structure_name is not None: #TODO check correct scope and declaration when is absent
                assign_code += f"this->{target} = {value};\n"
            if isinstance(node.value, ast.Lambda):
                assign_code+=f"auto {target} = {value[0]};\n"
                tm.add_to_scope(self.current_function_signature, self.current_structure_name, f"{target}{value[1]}", 'auto')
                tm.add_to_callableFunction(self.current_structure_name, self.current_function_name, target)
            elif target not in tm.pythonTypes_CppTypes:
                var_type=""
                if not tm.check_scope(self.current_function_signature, self.current_structure_name, target, node.value):#generate type for variable if it is not defined
                    var_type=tm.infer_type(node.value)#is not already declare
                    assign_code+=f"{var_type} "
                    tm.add_to_scope(self.current_function_signature,self.current_structure_name, target, var_type)
                assign_code += f"{target}{[] if var_type == 'char' else ''} = {value};\n"
        if self.current_function_signature is None: #assign is outside a function,method,class
            cppc.cppCodeObject.globalCode+=assign_code
        else:   #assing is inside a function,method,class
            return assign_code

    def visit_AnnAssign(self, node): #visit and translate to C++ AnnAssign node(es. c:int=0 or c:int;)
        #generate assign code
        var_name = self.visit(node.target)  #name variable
        self.array_single_type_declaration = True
        var_type = tm.get_type(self.visit(node.annotation)) #type variable
        self.array_single_type_declaration = False
        value = self.visit(node.value)  #value assign
        annAssign_code=self.indent()
        if isinstance(node.annotation, ast.List) and f"[{var_type}]" in tm.pythonTypes_CppTypesArrays: #array of a single type
            annAssign_code+= f"{var_type} {var_name}[] = " +'{'+value +"};\n"
            var_type=f"[{var_type}]"
        else:# f"{var_type}" not in tm.pythonTypes_CppTypesArrays:
            if var_type=="char":
                annAssign_code += f"{var_type} {var_name}[]" + (f" = {value}" if value != '' else "") + ";\n"
            else:
                annAssign_code += f"{var_type} {var_name}" + (f" = {value}" if value!='' else "") + ";\n" #assign with value and no value
        #add variable to typesMapping.scope
        tm.add_to_scope(self.current_function_signature,self.current_structure_name,var_name,f"{var_type}")

        if self.current_function_signature is None and self.current_structure_name is None: #annAssign is outside a function or class
            cppc.cppCodeObject.globalCode+=annAssign_code
        else:   #annAssign is inside a function or class
            return annAssign_code

    def visit_AugAssign(self, node):    #visit and translate to C++ AugAssign node(es: i+=<value)
        target = self.visit(node.target)        #variable
        op = self.visit(node.op)                #operator
        value = self.visit(node.value)          #value

        augAssign_code=f"{self.indent()}{target} {op}= {value};\n"
        if self.current_function_signature is None:  #augAssign is outside a function
            cppc.cppCodeObject.globalCode+=augAssign_code
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
        left = self.visit(node.left)   #left element to compare
        right = self.visit(node.comparators[0]) #right element to compare
        op = self.visit(node.ops[0])            #operator
        return f"{str(left)} {op} {str(right)}"


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
        print(tm.callableFunctions) #TODO remove, use for debugging
    except (ex.UnsupportedCommandError, ex.RecursiveFunctionError) as e:
        raise