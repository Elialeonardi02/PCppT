import ast
import typesMapping as tm
import exceptions as ex
import codeCpp.codeCppClass as cppc
from pcppt.codeCpp.codeCppClass import cppSupportClass


class astToCppParser(ast.NodeVisitor):

    def __init__(self): #constructor
        self.indent_level = 0                       #indent level of cpp code
        self.current_structure_name = None          #contain name of the exploring ClassDef node,
        self.current_function_name = None           #contain name of the exploring FunctionDef node,use for check recursive function
        self.current_function_signature=None        #contain function signature of the exploring FunctionDef Node, use for scope check

        #flag for array flexType
        self.array_multi_type_declaration = False   #true: value node to explore in AssignNode is a list, use for declaration of array flexType
        self.is_in_Compare=False                    #false: not exploring compareNode, true: exploring compareNode(if else), use for correct subscript in compare node of array flex type
        self.subscript_flexType_in_compare={}       #contain Subscript of array flexType to handle from a compare block, use for write the call to compare method with lambda functions

        # flag array single type
        self.array_single_type_declaration = False  # true: value node to explore in annAssignNode is a list, use for declaration of array single type

        #flag for map array
        self.is_mapArray=False                      #true: subscript node refer to MapArray(python dict), use in Assign node to write correctly subscript of MapArray
        self.mapArray_insert=False                  #true: subscrit node refer to mapArray ad is target of assign node, use in assign node for add (key, value) to MapArray
        self.mapArray_search=False                  #true: subscrit node refer to mapArray ad is value of assign node, use in assign node for search key in  MapArray

    def visit_Module(self, node):   #visit the root node of the AST
        for astNode in node.body:       #iterate through all the child nodes in the module body
            self.visit(astNode)         #visit each node

    def indent(self):   #generate an indentation string of space based on the current level of indentation to formate the code

        return "  " * self.indent_level

    def generic_visit(self, node):  #Called if no explicit visitor function exists for a node.
        #FIXME raise an exception when threre is not a function to explore the Node?
        return ""

    def visit_Name(self, node): #visit and translate to C++ Name node

        return node.id

    def visit_Num(self, node):  #visit and translate to C++ Num node

        return str(node.n)

    def visit_Constant(self, node):  #visit and translate to C++ Constant node
        if isinstance(node.value, str):
            return f"\"{node.value}\""
        return node.value

    def visit_Expr(self, node): # visit e translate in C++ Expr node

        return self.indent()+self.visit(node.value) + ";\n"

    def visit_ClassDef(self, node):  # visit e translate in C++ ClassDef node
        class_name = node.name
        self.current_structure_name = class_name                                                                        #save name of class for cppc.classes dictionary and scope dictionary

        #check the class is already defined
        if class_name not in cppc.cppCodeObject.classes:                                                                           #the class isn't already defined
            cppc.cppCodeObject.classes[class_name]=[{}]                                                                                #the first element of cppc.classes is {signature:body} of  functions
        else:                                                                                                           #the class is already defined
            raise ex.AlreadyDefinedError(class_name)
        self.indent_level += 1

        #parse attributes and methods
        for body_node in node.body:
            if isinstance(body_node, ast.AnnAssign):    #body_node is an attribute
                function_attribute_name=body_node.target.id #save name attribute
            elif isinstance(body_node, ast.FunctionDef):    #body_node is a method
                function_attribute_name = body_node.name    #save name method
            else:                                       #body_node is unsopported in class body
                raise ex.UnsupportedCommandError(node.body)

            body_node_code=self.indent()
            #visibility of fuction or attribute
            if len(function_attribute_name)>=2 and function_attribute_name[0]=='_' and function_attribute_name[1]!='_': #_<name> protected
                body_node_code += 'protected:'
            elif len(function_attribute_name)>=3 and function_attribute_name[0]=='_' and function_attribute_name[1]=='_'\
                    and function_attribute_name[-2:]!='__': #__<name> private
                body_node_code += 'private:'
            elif function_attribute_name is not None:   #<name> public
                body_node_code += 'public:'

            #add code to cppc
            if isinstance(body_node, ast.AnnAssign):                                                                        #is attribute
                body_node_code += self.visit(body_node)
                cppc.cppCodeObject.classes[class_name].append(body_node_code)                                                              #add code attribute to class list
            elif isinstance(body_node, ast.FunctionDef):                                                                    #is a method
                signature,method_body = self.visit(body_node)
                signature=body_node_code+signature                                                                              #add visibility to signature
                if signature not in cppc.cppCodeObject.classes[class_name][0]:                                                             #the method is not arleady defined
                    cppc.cppCodeObject.classes[class_name][0][signature]=f"\n{self.indent()}{method_body}"
                else:                                                                                                           #the method is arleady defined
                    raise ex.AlreadyDefinedError(f"in this class {signature}")

        #end of ClassDef node explorations
        self.indent_level -= 1
        self.current_structure_name=None

    def visit_FunctionDef(self, node):  #visit and translate to C++ FunctionDef node
        # save name for checking of recursive functions
        self.current_function_name = node.name
        #determine the function's type and name
        if node.returns is not None:                #type specified in Python source
            function_type = tm.pythonTypes_CppTypes.get(str(self.visit_returns(node.returns)))  #use typesMapping to traslate python type to c++ type
        else:                                       #type of function is not specified in the python source
            function_type = 'template <typename T> T'   #use template in c++
        if (self.current_structure_name is not None and #outside node is not a class
                (node.name=='__init__' or node.name==self.current_structure_name)): #function is a constructor of a class
            signature = f"{self.indent()}{self.current_structure_name}("    #signature construction
            tm.add_to_callableFunction(self.current_structure_name, self.current_structure_name)
        else:   #is a normal function or a method of a class
            signature = f"{self.indent()}{function_type} {node.name}(" #normal signature with type
            tm.add_to_callableFunction(self.current_structure_name, node.name)

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
        tm.add_to_scope(signature,self.current_structure_name)  #FIXME add function without parameter to scope
        for i in range(1 if self.current_structure_name is not None else 0, len(node.args.args)):                                           #start from 1 for methods to skip 'self'
            param_type = 'auto' if node.args.args[i].annotation is None else tm.pythonTypes_CppTypes.get(str(node.args.args[i].annotation.id))  #use 'auto' if type not specified #FIXME if the type is not specified raise an exception, type inference or use auto with vitis
            param_name = node.args.args[i].arg
            tm.add_to_scope(signature,self.current_structure_name,param_name,param_type)

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
            else:                                                                                                                                   #function is already defined
                raise ex.AlreadyDefinedError(signature)
            cppc.cppCodeObject.functions[signature]=func_code
        else:                                                                                                                                   #is a method of a class
            return signature, func_code


        #end of functionDef node explorations
        self.current_function_name = None
        self.current_function_signature = None

    def visit_Call(self, node):  #visit and translate to C++ Call node(function call)
        #recursive function check
        function_name= self.visit(node.func)    #get the name of the function being called
        if function_name==self.current_function_name:   #is recursive function
            raise ex.RecursiveFunctionError(function_name)

        #check if the function is supported
        if(self.current_structure_name is not None):    #FIXME check of method call on instance doesn't work
            tm.check_callableFunction(function_name)

        #parameters of the call
        args = [str(self.visit(arg)) for arg in node.args]

        return f"{function_name}({', '.join(args)})"

    def visit_For(self, node):  #visit and translate to C++ For node
        target = self.visit(node.target)    #loop counter
        iter_value = self.visit(node.iter)  #iterator (range)
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
        elif self.array_multi_type_declaration:
            elements = [f"{{{tm.corret_value(self.visit(el))}}}" for el in node.elts]
            return f"{{{', '.join(elements)}}}"
        else:
            elements = [f"{tm.corret_value(self.visit(el))}" for el in node.elts]
            return f"{', '.join(elements)}"

    def visit_Dict(self, node):
        dictionary={}
        for k,v in zip(node.keys,node.values):
            dictionary[self.visit(k)]=self.visit(v)
        return  dictionary

    def visit_Subscript(self, node):    #visit and translate to C++ Subscript node (accessing elements) #FIXME add sintax for code outside of a function
        obj = self.visit(node.value)          #the object being indexed
        index = self.visit(node.slice)    #the index to access
        type=tm.get_var_type_scope(self.current_function_signature,self.current_structure_name,obj)
        if type in tm.pythonTypes_CppTypesArrays:
            return f"{obj}[{index}]"
        elif type==f"[{cppc.cppSupportClass['flexType']}]":
            if not self.is_in_Compare:
                return f"{obj}[{index}].{cppc.cppSupportClass['get']}"
            else:
                self.subscript_flexType_in_compare[f"{obj}[{index}]"]=cppc.cppSupportClass['flexType']+obj+str(index)
                return cppc.cppSupportClass['flexType']+obj+str(index)
        elif type==cppc.cppSupportClass['dict'] :
            self.is_mapArray=True
            if self.mapArray_insert:
                return f"{obj}.{cppc.cppSupportClass['mapInsert']}({index},"
            elif self.mapArray_search:
                return f"*{obj}.{cppc.cppSupportClass['mapSearch']}({index})"
        else:
            return [f"{self.visit(node.value)}[{self.visit(node.slice)}]"]


    def visit_Attribute(self, node):  #visit and translate to C++ Attribute node
        if self.current_structure_name is None:
            value = self.visit(node.value)
        else:
            value='this'
        attr_name = node.attr
        return f"{value}{'->' if self.current_structure_name is not None else '.'}{attr_name}"  #FIXME not correct if use istance of other class

    def visit_targets(self, node):  #visit and traslate to C++ targets elements. It is not a fuction of AST library
        targets=[]
        if isinstance(node[0], ast.Tuple):
             for el in node[0].elts:
                 targets.append(el.id)
        elif isinstance(node[0],ast.Attribute):
            return[node[0].attr], None
        elif isinstance(node[0],ast.Name):
            for el in node:
                targets.append(el.id)
        elif isinstance(node[0],ast.Subscript):
            return [self.visit(node[0])],node[0].value.id
        return targets, None

    def visit_Assign(self, node):   #visit and translate to C++ Assign node
        self.mapArray_insert=True
        targets, var_name = self.visit_targets(node.targets)#left variable or variables
        self.mapArray_insert=False
        self.mapArray_search=True
        value = self.visit(node.value)
        self.mapArray_search=False
        assign_code = self.indent()
        var_type = tm.get_var_type_scope(self.current_function_signature, self.current_structure_name, var_name)
        if isinstance(node.value,ast.List) and len(targets)==1 and isinstance(node.targets[0],ast.Name) : #is an array multi typedeclaration
            self.array_multi_type_declaration=True
            value = self.visit(node.value)
            #FIXME handler when is already defined,
            var_type=cppSupportClass['flexType']
            assign_code+=f"{var_type} {targets[0]}[]= {value};\n"
            tm.add_to_scope(self.current_function_signature, self.current_structure_name,targets[0],f"[{var_type}]")
            self.array_multi_type_declaration=False
        elif len(targets)==1 and isinstance(node.targets[0],ast.Subscript) and var_type==cppc.cppSupportClass['flexType']:  #assign value to array flexType element
            if var_type not in tm.pythonTypes_CppTypesArrays:
                    assign_code += f"{targets[0]}.{cppc.cppSupportClass['set']}({value});\n"
            elif var_type in tm.pythonTypes_CppTypesArrays:
                    assign_code+=f"{targets[0]}={value};\n"
        elif self.is_mapArray:
            if len(targets)==1 and isinstance(node.targets[0],ast.Subscript) and var_type == cppc.cppSupportClass['dict']:  # assign value to arrayMap
                assign_code+=f"{targets[0]} {value});\n"
            elif isinstance(node.value,ast.Subscript):
                assign_code += f"{targets[0]} = {value};\n"
            self.is_mapArray=False
        elif isinstance(node.value,ast.Subscript) :  #assign array multitype value to variable
            assign_code+=f"{value}({targets[0]});\n"
        else:#common assign code
            for target in targets:
                if isinstance(node.targets[0],ast.Attribute) and self.current_structure_name is not None: #TODO check correct scope and declaration when is absent
                    assign_code += f"this->{target} = {value};\n"
                elif target not in tm.pythonTypes_CppTypes:
                    var_type=""
                    if not tm.check_scope(self.current_function_signature, self.current_structure_name, target, node.value):#generate type for variable if it is not defined
                        var_type=tm.infer_type(node.value)#is not already declare
                        assign_code+=f"{var_type} "
                        tm.add_to_scope(self.current_structure_name,self.current_function_signature, target, var_type)

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
        elif isinstance(node.annotation, ast.Dict):
            key_type = next(iter(var_type))
            value_type = var_type[key_type]
            annAssign_code+=f"{cppc.cppSupportClass['dict']}<{key_type},{value_type},{len(value)}> {var_name}(\n"
            self.indent_level+=1
            for i, k in enumerate(value):
                annAssign_code += f"{self.indent()}{cppc.cppSupportClass['dictStruct']}<{key_type},{value_type}>({k},{value[k]})"
                if i < len(value) - 1:
                    annAssign_code += ',\n'
                else:
                    self.indent_level-=1
                    annAssign_code += f"\n{self.indent()});\n"
            var_type=cppc.cppSupportClass['dict']
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
        self.is_in_Compare=True
        left = self.visit(node.left)   #left element to compare
        right = self.visit(node.comparators[0]) #right element to compare
        op = self.visit(node.ops[0])            #operator
        self.is_in_Compare = False
        if len(self.subscript_flexType_in_compare)==0:
            return f"{str(left)} {op} {str(right)}"
        else:
            k,v=next(iter(self.subscript_flexType_in_compare.items()))
            self.subscript_flexType_in_compare={}
            return f"{k}.{cppc.cppSupportClass['compare']}([](auto {v})->bool"+"{"+f"return {str(left)} {op} {str(right)};"+"})"


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