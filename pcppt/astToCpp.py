import ast

import typesMapping as tm
import exceptions as ex
import codeCpp.codeCppClass as cppc
from pcppt.typesMapping import check_scope


class astToCppParser(ast.NodeVisitor):

    def __init__(self): #constructor
        self.indent_level = 0                       #indent level of cpp code
        self.current_structure_name = None          #contain name of the exploring ClassDef node,
        self.current_function_name = None           #contain name of the exploring FunctionDef node,use for check recursive function
        self.current_function_signature=None        #contain function signature of the exploring FunctionDef Node, use for scope check

        # flag array single type
        self.array_single_type_declaration = False  # true: value node to explore in annAssignNode is a list, use for declaration of array single type

        #array body class
        self.protected = {'attributes': [], 'methods': {}}
        self.private = {'attributes': [], 'methods': {}}
        self.public = {'attributes': [], 'methods': {}}

    def indent(self):   #generate an indentation string of space based on the current level of indentation to formate the code

        return "  " * self.indent_level

    #ast visit
    def visit_Module(self, node):   #visit the root node of the AST
        for astNode in node.body:       #iterate through all the child nodes in the module body
            self.visit(astNode)         #visit each node

    def generic_visit(self, node):  #Called if no explicit visitor function exists for a node.

        return ""

    def visit_FunctionDef(self, node):  #visit and translate to C++ FunctionDef node
        # save name for checking -of recursive functions
        self.current_function_name = node.name

        #determine function type and name
        if node.returns is not None:    #type specified in Python source
            function_type = tm.get_type(str(self.visit_returns(node.returns)))  #use typesMapping to traslate python type to c++ type
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
            param_type = 'auto' if node.args.args[i].annotation is None else tm.get_type(str(node.args.args[i].annotation.id))  #use 'auto' if type not specified #FIXME if the type is not specified raise an exception, type inference or use auto with vitis
            param_name = node.args.args[i].arg
            signature += f"{param_type} {param_name}"
            if i < len(node.args.args) - 1: #it is not last parameter
                signature += ', '
        signature += ')'

        #add parameters to scope of the function in typesMapping.scope
        self.current_function_signature = signature
        signature=self.indent()+signature

        for i in range(0, len(node.args.args)): #start from 1 for methods to skip 'self'
            param_type = 'auto' if node.args.args[i].annotation is None else tm.get_type(str(node.args.args[i].annotation.id))  #use 'auto' if type not specified #FIXME if the type is not specified raise an exception, type inference or use auto with vitis
            param_name = node.args.args[i].arg
            if param_name=='self': #i==1
                tm.add_to_scope(self.current_function_signature,self.current_structure_name)
            else:
                tm.add_to_scope(self.current_function_signature, self.current_structure_name,param_name,param_type)

        func_code = f"{self.indent()}{{\n"
        # body of the function

        self.indent_level += 1
        for astNode in node.body:
            if not isinstance(astNode, ast.FunctionDef):    #the node is not a def of a function
                iBodyCode=self.visit(astNode)
                func_code += iBodyCode
            else:   #a function declaration in the body
                temp_indent_level=self.indent_level
                self.indent_level=0
                self.visit(astNode)
                self.indent_level=temp_indent_level
                self.current_function_name = node.name  #reset current_function_name to current signature after visit
                self.current_function_signature = signature

        self.indent_level -= 1
        func_code += self.indent() + "}\n"



        # end of functionDef node explorations
        self.current_function_name = None
        self.current_function_signature = None

        # save signature and func_code in cppc
        if self.current_structure_name is None: #is a function
            if signature not in cppc.cppCodeObject.functions:   #function is not already defined
                cppc.cppCodeObject.functions[signature] = ''
            else:   #FIXME it is the same control of tm.add_to_scope
                raise ex.AlreadyDefinedError(signature)
            cppc.cppCodeObject.functions[signature]=func_code
        else:   #is a method of a class
            return signature, func_code




    def visit_ClassDef(self, node):  # visit e translate in C++ ClassDef node
        self.current_structure_name = node.name #save name of class for cppc.classes dictionary and scope

        #check class is already defined
        if self.current_structure_name not in cppc.cppCodeObject.classes:   #class isn't already define
            cppc.cppCodeObject.classes[self.current_structure_name]={}       #add class to scope
        else:                                                               #class already define
            raise ex.AlreadyDefinedError(self.current_structure_name)
        self.indent_level += 1

        #parse attributes and methods
        for body_node in node.body:
            if isinstance(body_node, ast.AnnAssign):    #body_node is an attribute
                body_node_code = self.visit(body_node)
                self.classDef_add_AnnAssign(body_node_code,body_node.target.id)
            elif isinstance(body_node, ast.FunctionDef):    #body_node is a method
                signature,method_body = self.visit(body_node)
                self.classDef_add_FunctionDef(signature,method_body,body_node.name)
            else:                                       #body_node is unsopported in class body
                raise ex.UnsupportedCommandError(node.body)

        #is not a constructor defined
        if not(tm.check_callableFunction(self.current_structure_name,'__init__','__init__')):   #FIXME correct __init__ with name of the class
            constructor_code = ""
            for var, type in tm.scope[self.current_structure_name].items():
                if not isinstance(type, dict):
                    constructor_code += f"{var}({tm.cppTypes_DefaultsValues.get(type)}),"
            if constructor_code != "":  #class with parameters
                constructor_code = {f"{self.indent()}{self.current_structure_name}()":f"{self.indent()}:{constructor_code.rstrip(',')} {{}}\n"}
            else:   #class without parameters   #FIXME remove
                constructor_code = {f"{self.indent()}{self.current_structure_name}()": f"{self.indent()} = default;\n"}

            self.public['methods'] = {**constructor_code, **self.public['methods']}

        #end of ClassDef node explorations
        if self.protected['attributes'] or self.protected['methods']:
            cppc.cppCodeObject.classes[self.current_structure_name]['protected']=self.protected
        if self.private['attributes'] or self.private['methods']:
            cppc.cppCodeObject.classes[self.current_structure_name]['private']=self.private
        if self.public['attributes'] or self.public['methods']:
            cppc.cppCodeObject.classes[self.current_structure_name]['public']=self.public

        self.protected = {'attributes': [], 'methods': {}}
        self.private = {'attributes': [], 'methods': {}}
        self.public = {'attributes': [], 'methods': {}}
        self.indent_level -= 1
        self.current_structure_name=None

    def visit_Return(self, node):   #visit and translate to C++ Return node

        return f"{self.indent()}return {self.visit(node.value)};\n"

    def visit_Assign(self, node):   #visit and translate to C++ Assign node
        targets= self.visit_targets(node.targets)#left variable or variables
        value = self.visit(node.value)
        assign_code = ""
        for itarget, target in enumerate(targets):
            assign_code +=self.indent()
            if (isinstance(node.targets[0],ast.Tuple) and isinstance(node.targets[0].elts[itarget],ast.Attribute)) or isinstance(node.targets[0],ast.Attribute) :   #target attribute inside a class, or tuple declaration of attribute
                assign_code += f"{target['code']} = {value};\n"
                if target['value']=='self' and not tm.check_scope(None, self.current_structure_name,target['attr']): #attribute of self class
                    var_type = tm.infer_type(node.value, value)
                    temp_indent = self.indent_level
                    self.indent_level = 1
                    if isinstance(node.value, ast.List):
                        assign_code=''
                        self.classDef_add_AnnAssign(
                             f"{self.indent()}{var_type} {target['attr']}[{len(node.value.elts)}]={{{value}}};\n", target['attr'])
                        var_type = f"[{var_type}]"
                    else:
                        self.classDef_add_AnnAssign(f"{self.indent()}{var_type} {target['attr']};\n", target['attr'])
                    tm.add_to_scope(self.current_function_signature if target['value']!='self' else None , self.current_structure_name, target['attr'], var_type)
                    self.indent_level = temp_indent
                elif target['value']!='self':
                   if  not tm.check_scope(self.current_function_signature, self.current_structure_name,target['value']): #undefined instance
                       raise ex.IsNotDefinedError(target['value'])
                   elif not tm.check_scope(None, tm.get_var_type_scope(self.current_function_signature, self.current_structure_name,target['value']),target['attr']): #istance defined but the method is not defined in the class of the instance
                       raise ex.IsNotDefinedError(f"{target['attr']} in class or struct {target['value']}")


            elif isinstance(node.value, ast.Lambda):    #declare lambda function
                assign_code+=f"auto {target} = {value[0]};\n"
                tm.add_to_scope(self.current_function_signature, self.current_structure_name, f"{target}{value[1]}", 'auto')
                tm.add_to_callableFunction(self.current_structure_name, self.current_function_name, target)
            elif isinstance(node.value,ast.List):
                if not tm.check_scope(self.current_function_signature, self.current_structure_name, target.split("[")[0]):#generate type for variable if it is not defined #.split("[")[0] for check array(subscript) in scope
                    var_type = tm.infer_type(node.value,value)  # is not already declare
                    if var_type=='char':    #array string
                        assign_code += f"const {var_type}* {target}[{len(node.value.elts)}] = {{{value}}};\n"
                    else:   #common array
                        assign_code+=f"{var_type} {target}[{len(node.value.elts)}] = {{{value}}};\n"
                    tm.add_to_scope(self.current_function_signature, self.current_structure_name, target, f"[{var_type}]")
                else:   #array is already define, can't assign array to list already defined, make a temp array to assign value to target
                    temp_indent=self.indent_level
                    var_type = tm.infer_type(node.value,value)
                    self.indent_level += 1
                    assign_code+=f"{{\n{self.indent()}{var_type} temp_array_assign[{len(node.value.elts)}] = {{{value}}};\n"
                    assign_code+=f"{self.indent()}for (int i=0; i<{len(node.value.elts)}; i++) {{\n"
                    self.indent_level += 1
                    assign_code += f"{self.indent()}{target}[i] = temp_array_assign[i];\n"
                    self.indent_level -= 1
                    assign_code+=f"{self.indent()}}}\n"
                    self.indent_level -= 1
                    assign_code += f"{self.indent()}}}\n"

                    self.indent_level=temp_indent
            else:
                if not tm.check_scope(self.current_function_signature, self.current_structure_name, target) and not tm.check_scope(self.current_function_signature, self.current_structure_name, target.split("[")[0]): #TODO move check scope for subscript?
                    var_type = tm.infer_type(node.value,value)  # is not already declare
                    assign_code += f"{var_type} "
                    tm.add_to_scope(self.current_function_signature,self.current_structure_name, target, var_type)
                    assign_code += f"{target}{[] if var_type == 'char' else ''} = {value};\n"
                else:
                    assign_code += f"{target} = {value};\n"
        if self.current_function_signature is None: #assign is outside a function,method,class
            cppc.cppCodeObject.globalCode+=assign_code
        else:   #assing is inside a function,method,class
            return assign_code

    def visit_AugAssign(self, node):    #visit and translate to C++ AugAssign node(es: i+=<value)
        target = self.visit(node.target)        #variable
        op = tm.get_operator(node.op)           #operator
        value = self.visit(node.value)          #value

        augAssign_code=f"{self.indent()}{target} {op}= {value};\n"
        if self.current_function_signature is None:  #augAssign is outside a function
            cppc.cppCodeObject.globalCode+=augAssign_code
        else:
            return augAssign_code               #augAssign is inside a function

    def visit_AnnAssign(self, node): #visit and translate to C++ AnnAssign node(es. c:int=0 or c:int;)
        #generate assign code
        var_name = self.visit(node.target)  #name variable
        self.array_single_type_declaration = True
        annotation = self.visit(node.annotation) #annotation array
        var_type=tm.get_type(annotation[0] if isinstance(node.annotation,ast.List) else annotation)  #type
        dim_array=annotation[1] if len(annotation) > 1  else ""    #dimension of array, if specified
        self.array_single_type_declaration = False
        value = self.visit(node.value)  #value assign
        annAssign_code=self.indent()
        if isinstance(node.annotation, ast.List) and(var_type in tm.pythonTypes_CppTypes or var_type in cppc.cppCodeObject.classes): #array of a single type
            annAssign_code+= f"{var_type} {var_name}[{dim_array}] = " +'{'+value +"};\n"
            var_type=f"[{var_type}]"
        else:# f"{var_type}" not in tm.pythonTypes_CppTypesArrays:
            if len(annotation) > 1 and var_type=='char':    #array string, const
                annAssign_code += f"const {var_type}* {var_name}[{dim_array}]" + (f" = {{{value}}}" if value != '' else "") + ";\n"
            elif var_type=="char":
                annAssign_code += f"{var_type} {var_name}[]" + (f" = {value}" if value != '' else "") + ";\n"   #FIXME str parsing
            else:#assign with value and no value
                annAssign_code  += f"{var_type}{'*' if var_type in tm.scope else ''} {var_name}" + (f" = {value}" if value != '' else "") + ";\n"   #

        #add variable to typesMapping.scope
        tm.add_to_scope(self.current_function_signature,self.current_structure_name,var_name,f"{var_type}")

        if self.current_function_signature is None and self.current_structure_name is None: #annAssign is outside a function or class
            cppc.cppCodeObject.globalCode+=annAssign_code
        else:   #annAssign is inside a function or class
            return annAssign_code

    def visit_For(self, node):  #visit and translate to C++ For node
        target = self.visit(node.target)    #loop counter
        iter_values = []
        #target type_inference #TODO add more type
        types=[]
        type_target='int'
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

    def visit_While(self, node):  #visit and translate to C++ While node
        loop_code=f"{self.indent()}while({self.visit(node.test)}){{\n"    #compare whail
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

    def visit_Expr(self, node): # visit e translate in C++ Expr node

        return self.indent()+self.visit(node.value) + ";\n"

    def visit_Break(self, node):    #visit and traslate to c++ Break node

        return f"{self.indent()}break;\n"

    def visit_Continue(self, node):  #visit and traslate to c++ Continue node

        return f"{self.indent()}continue;\n"

    def visit_Pass(self, node):

        return f"\n";

    def visit_BoolOp(self, node):   #visit and translate to C++ BoolOp node
        op = tm.get_operator(node.op)                               #operator
        values = [self.visit(value) for value in node.values]   #values

        return f" {op} ".join(values)

    def visit_BinOp(self, node):    #visit and translate to C++ BinOp node
        left = self.visit(node.left)    #left member
        right = self.visit(node.right)  #right member
        op = tm.get_operator(node.op)    #operator
        if isinstance(node.op, ast.FloorDiv):   #floor division parsing
            return f"({left}<0) ? ({left}-{right} +1 ) /{right} : {left}/{right}"   #FIXME round correct?
        else:
            return f"{left} {op} {right}"

    def visit_UnaryOp(self, node):
        op = tm.get_operator(node.op)  # operator
        operand = self.visit(node.operand) # values

        return f"{op}{operand}"

    def visit_Lambda(self, node):
        # parameters and types of the function
        signature="("
        for i, arg in enumerate(node.args.args):
            signature += f"auto {arg.arg}"
            if i < len(node.args.args) - 1:  # Aggiunge una virgola se non è l'ultimo parametro
                signature += ', '
        signature += ")"
        return  f"[]{signature} {{{self.visit(node.body)};}}",signature

    def visit_IfExp(self,node):
        condition = self.visit(node.test)
        body = self.visit(node.body)
        orelse = self.visit(node.orelse)
        return f"{self.indent()}({condition} ? {body} : {orelse});\n"

    def visit_Dict(self, node):
        dictionary={}
        for k,v in zip(node.keys,node.values):
            dictionary[self.visit(k)]=self.visit(v)
        return dictionary

    def visit_Compare(self, node):  #visit and translate to C++ Compare node
        left = self.visit(node.left)
        right = []

        for op, comparator in zip(node.ops, node.comparators): #multiple comparisons in a chain
            op_str = tm.get_operator(op)
            comp_str = self.visit(comparator)
            right.append(f"{str(left)} {op_str} {str(comp_str)}")
            left = comp_str
        if len(right) == 1:
            return right[0]
        return " && ".join(right)

    def visit_Call(self, node):  #visit and translate to C++ Call node(function call)
        #recursive function check
        function_name= self.visit(node.func)    #get the name of the function being called
        if function_name==self.current_function_name:   #is recursive function
            raise ex.RecursiveFunctionError(function_name)

        #check if the function is supported
        if not tm.check_callableFunction(self.current_structure_name, self.current_function_name, function_name) and function_name not in cppc.cppCodeObject.classes and isinstance(node.func,ast.Name): #FIXME raise when func is not only a name
            raise ex.NotCallableError(function_name)

        if function_name in tm.scope:
            function_name=f"new {function_name}"
        #parameters of the call
        args = [str(self.visit(arg)) for arg in node.args]

        return f"{function_name}({', '.join(args)})"

    def visit_FormattedValue(self,node):#visit and translate to c++ FormattedValue in JoinedString node
        return f"{self.visit(node.value)}"

    def visit_JoinedStr(self,node): #visit and translate to c++ JoinedStr node(f" ")    #FIXME doesn't work
        code_joinedStr=''
        for value in node.values:
            code_joinedStr+=f"<<{self.visit(value)}"
        return code_joinedStr

    def visit_Constant(self, node):  #visit and translate to C++ Constant nod
        if isinstance(node.value, str): #parse for string declaration
            return f"\"{node.value}\""
        elif isinstance(node.value, bool): #parsing bool
            return tm.parsing_constant[node.value]
        return node.value

    def visit_Attribute(self, node):  #visit and translate to C++ Attribute node
        value = self.visit(node.value)
        if value=='self' :
            value='this->'
        else:
            value=f"{value}."
        return f"{value}{node.attr}"  #FIXME not correct if use instance of other class


    def visit_Subscript(self, node):    #visit and translate to C++ Subscript node (accessing elements)
        obj = self.visit(node.value)          #the object being indexed
        index = self.visit(node.slice)    #the index to access
        #type=tm.get_var_type_scope(self.current_function_signature,self.current_structure_name,obj)
        #if type in tm.pythonTypes_CppTypesArrays:
        return f"{obj}[{index}]"

    def visit_Name(self, node): #visit and translate to C++ Name node

        return node.id

    def visit_List(self, node):
        if self.array_single_type_declaration:  # is type of array one type element declaration
            return [f"{self.visit(el)}" for el in node.elts]
        else:
            elements = [f"{tm.corret_value(self.visit(el))}" for el in node.elts]
            return f"{', '.join(elements)}"

    def visit_Dict(self, node):
        dictionary = {}
        for k, v in zip(node.keys, node.values):
            dictionary[self.visit(k)] = self.visit(v)
        return dictionary

    def visit_Num(self, node):  #visit and translate to C++ Num node

        return str(node.n)

    #support functions
    def visit_returns(self, node):  # part of Return node
        if isinstance(node, ast.Name):
            return self.visit_Name(node)
        elif isinstance(node, ast.Constant):
            return str(self.visit_Constant(node))

    def visit_targets(self, node):  # visit and traslate to C++ targets elements. It is not a fuction of AST library
        targets = []
        if isinstance(node[0], ast.Tuple):
            for el in node[0].elts:
                if isinstance(el, ast.Attribute):  # elem in a tuple is attribute class
                    targets.append({'attr':el.attr,'code':self.visit(el),'value':self.visit(el.value)})
                else:
                    targets.append(el.id)
        elif isinstance(node[0], ast.Attribute):
            return [{'attr':node[0].attr,'code':self.visit(node[0]),'value':self.visit(node[0].value)}]
        elif isinstance(node[0], ast.Name):
            for el in node:
                targets.append(el.id)
        elif isinstance(node[0], ast.Subscript):
            return [self.visit(node[0])]
        return targets

    def classDef_add_AnnAssign(self, body_node_code,function_attribute_name):
        if len(function_attribute_name) >= 2 and function_attribute_name[0] == '_' and function_attribute_name[1] != '_':  # _<name> -> protected
            self.protected['attributes'].append(body_node_code)
        elif len(function_attribute_name) >= 3 and function_attribute_name[0] == '_' and function_attribute_name[ 1] == '_' and function_attribute_name[-2:] != '__':  # __<name> -> private
            self.private['attributes'].append(body_node_code)
        elif function_attribute_name is not None:  # <name> -> public
            self.public['attributes'].append(body_node_code)

    def classDef_add_FunctionDef(self, signature,method_body, function_attribute_name):
        if len(function_attribute_name) >= 2 and function_attribute_name[0] == '_' and function_attribute_name[1] != '_':  # _<name> -> protected
            self.protected['methods'][signature] = method_body
        elif len(function_attribute_name) >= 3 and function_attribute_name[0] == '_' and function_attribute_name[1] == '_' and function_attribute_name[-2:] != '__':  # __<name> -> private
            self.private['methods'][signature] = method_body
        elif function_attribute_name is not None:  # <name> -> public
            self.public['methods'][signature] = method_body
def generateAstToCppCode(python_ast):
    try:
        astToCppParser().visit(python_ast)
        print(tm.scope) #TODO remove, use for debugging
        print(tm.callableFunctions) #TODO remove, use for debugging
    except (ex.UnsupportedCommandError, ex.RecursiveFunctionError) as e:
        raise