from enum import Enum
import ast
from pcppt import exceptions as ex, typesMapping as tm, codeCppClass as cppc
#use to identify correct operator
class FOperatorKind(Enum):
    NONE = 1
    FILTER = 3
    MAP = 4
    FLAT_MAP = 5

def visit_FunctionDef(self, node):  #visit and translate to C++ FunctionDef node
        # save name for checking recursive functions
        self.current_function_name = node.name

        #chose to parse function
        toparse=True
        if not self.transplile_class and self.current_function_signature is None:
            if not node.decorator_list :
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name) and str(self.visit(decorator).lower().replace(" ", "") == "wireflow") :   #pars only function and method with decorator "wireflow"
                        break
                    toparse=False
        if not toparse:
            return False,False #to stop parsing method of a class

        #determine function name
        if (self.current_structure_name is not None and #outside node is not a class
                (node.name=='__init__' or node.name==self.current_structure_name)): #function is a constructor of a class
            signature = f"{self.current_structure_name}("    #signature construction
        elif node.name=='__call__' and self.operator!=FOperatorKind.NONE:
            signature = f"operator()("
        else:   #is a normal function or a method of a class
            signature = f"{node.name}(" #normal signature with type


        #parameters and types of the function
        if node.name!='__call__' or self.operator == FOperatorKind.NONE:
            #list of const and reference
            wireflow_refs=[]
            wireflow_const=[]
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    for type_node in decorator.args:
                        type=self.visit(type_node)
                        if isinstance(decorator.func,ast.Attribute):
                            func = decorator.func.attr
                        else:
                            func = self.visit(decorator.func)
                        if (func == 'param_const' or func == 'param_cref') and type not in wireflow_const:
                            wireflow_const.append(type)
                        if (func == 'param_ref' or func == 'param_cref') and type not in wireflow_refs:
                            wireflow_refs.append(type)
            for i in range(1 if self.current_structure_name is not None else 0, len(node.args.args)):   #start from 1 for methods to skip 'self'
                param_name = node.args.args[i].arg
                if node.args.args[i].annotation is None:    #type of parameter is not defined
                    param_type = 'auto'
                else:
                    param_type=''

                    #parameter const
                    annotation=str(self.visit(node.args.args[i].annotation))
                    if annotation in wireflow_const:
                        param_type += f"const "

                    #array parameter
                    if isinstance(node.args.args[i].annotation,ast.List):
                        self.array_dimensions=True
                        annotation = self.visit(node.args.args[i].annotation)  # annotation array
                        self.array_dimensions = False
                        param_type+=tm.get_type(annotation[0])
                        if len(annotation)==2:#array monodimensional [<type>,<dim>}
                            param_name+=f"[{annotation[1]}]"
                        elif len(annotation)==3: #array matrix  [<type>, <rows>,<colums>]
                            param_name+=f"[{annotation[1]}][{annotation[2]}]"
                        else:
                            raise ex.UnsupportedCommandError(f"cannot defined array: {node.args.args[i].arg} with {len(annotation)-1} dimension" )
                    else: #common parameter
                        param_type+=tm.get_type(annotation)

                    #parameter reference
                    if annotation in wireflow_refs:
                        param_type+=' &'
                signature += f"{param_type} {param_name}"

                # default value for parameter
                if (self.current_structure_name is not None and i > 0) or self.current_structure_name is None:
                    pv = len(node.args.args) - i - 1
                    if pv < len(node.args.defaults) and node.args.defaults[pv] is not None:
                        value = self.visit(node.args.defaults[pv])
                        if isinstance(node.args.defaults[pv], ast.List):
                            raise ex.UnsupportedCommandError(f"array default value [{value}] for {param_name}")
                        signature += f" = {value}"

                if i < len(node.args.args) - 1: #it is not last parameter
                    signature += ', '

            signature += ')'


            #add parameters to scope of the function in typesMapping.scope
            self.current_function_signature = signature
            for i in range(0, len(node.args.args)): #start from 1 for methods to skip 'self'
                param_name = node.args.args[i].arg
                if node.args.args[i].annotation is None:
                    param_type = 'auto'
                else:
                    if isinstance(node.args.args[i].annotation, ast.List):  # array parameter
                        self.array_dimensions = True
                        annotation = self.visit(node.args.args[i].annotation)  # annotation array
                        self.array_dimensions = False
                        param_type = f"[{tm.get_type(annotation[0])}]"
                    else:
                        param_type = tm.get_type(str(self.visit(node.args.args[i].annotation)))  # use 'auto' if type not specified
                if param_name!='self': #i==1
                    tm.add_to_scope(self.current_function_signature, self.current_structure_name,param_name,param_type)
        else: #parse operator and add parameters to tm.scope
            p1={'name': node.args.args[1].arg  , 'type': self.visit(node.args.args[1].annotation)}
            p2={'name': node.args.args[2].arg , 'type': self.visit(node.args.args[2].annotation)}
            tm.add_to_scope(self.current_function_signature, self.current_structure_name, p1['name'], p1['type'])
            signature += f"const {p1['type']} & {p2['name']}, "
            if self.operator.name == FOperatorKind.MAP.name or self.operator.name == FOperatorKind.FILTER.name:
                tm.add_to_scope(self.current_function_signature, self.current_structure_name, p2['name'], p2['type'])
                signature += f"{p2['type']} & {p2['name']})"
            if self.operator.name == FOperatorKind.FILTER.name:
                p3_name = node.args.args[3].arg
                signature = f"{signature[:-1]}, bool & {p3_name})"
                tm.add_to_scope(self.current_function_signature, self.current_structure_name, p3_name, 'bool')
            if self.operator.name == FOperatorKind.FLAT_MAP.name:
                signature+= f"shipper_t<T> & {p2['name']})"
                tm.add_to_scope(self.current_function_signature, self.current_structure_name, p2['name'], 'shipper_t')

        # body of the function
        func_code = f"{self.indent()}{{\n"
        self.indent_level += 1
        function_type = ""
        for astNode in node.body:
            if not isinstance(astNode, ast.FunctionDef):  # the node is not a def of a function
                iBodyCode = self.visit(astNode)
                func_code += iBodyCode
                if node.returns is None and isinstance(astNode, ast.Return):
                    function_type = tm.infer_type(astNode.value,None, self.current_structure_name,self.current_function_signature)
            else:  # a function declaration in the body
                temp_indent_level = self.indent_level
                if self.current_structure_name is None: #is a function
                    self.indent_level = 0
                else:   #is a method of a class
                    self.indent_level = 1
                self.visit(astNode)
                self.indent_level = temp_indent_level
                self.current_function_name = node.name  # reset current_function_name to current signature after visit
                self.current_function_signature = signature
        self.indent_level -= 1
        func_code += self.indent() + "}\n"

        # determine function type
        if node.returns is not None:  # type specified in Python source
            function_type = tm.get_type(str(self.visit_returns(node.returns)))  # use typesMapping to traslate python type to c++ type #FIXME handler return type array pointer?
        else:  # type of function is not specified in the python source
            if function_type=="":  # is not return in body of the functions
                function_type = 'void'
            elif function_type=="auto":
                function_type = 'template <typename T> T'  # use template in c++
        if node.name == '__call__' and self.operator != FOperatorKind.NONE:
            signature = f"{self.indent()}void {signature}"
            if self.operator.name == FOperatorKind.FLAT_MAP.name:
                signature = f"{self.indent()}template <typename T>\n{signature}"
        elif node.name!='__init__':  # is a normal function or a method of a class
            signature = f"{self.indent()}{function_type} {signature}"  # normal signature with type

        # save signature and func_code in cppc
        if self.current_structure_name is None: #is a function
            tm.add_to_callableFunction(None, None,self.current_function_name, function_type)
            if signature not in cppc.cppCodeObject.functions:   #function is not already defined
                cppc.cppCodeObject.functions[signature] = ''
            else:   #FIXME it is the same control of tm.add_to_scope
                raise ex.AlreadyDefinedError(signature)
            cppc.cppCodeObject.functions[signature]=func_code
        else:   #is a method of a class
            tm.add_to_scope(self.current_function_signature,self.current_structure_name, f"{self.current_structure_name}.{self.current_function_name}", function_type)
            tm.add_to_callableFunction(self.current_structure_name,None, f"{self.current_structure_name}.{self.current_function_name}", function_type)
            self.classDef_add_FunctionDef(signature,func_code,self.current_function_name)

        # end of functionDef node explorations
        self.current_function_name = None
        self.current_function_signature = None

def visit_ClassDef(self, node):  # visit e translate in C++ ClassDef node

    #check class is already defined
    if node.name in tm.scope:
        raise ex.AlreadyDefinedError(f"class {node.name}")

    self.protected = {'attributes': [], 'methods': {}}
    self.private = {'attributes': [], 'methods': {}}
    self.public = {'attributes': [], 'methods': {}}

    self.tempAttributesDeclaretions = {}

    if node.decorator_list:
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and str(self.visit(decorator).lower().replace(" ", "") == "wireflow") :   #pars only function and method with decorator "wireflow"
                self.transplile_class = True

    self.current_structure_name = node.name #save name of class for cppc.classes dictionary and scope
    self.indent_level += 1

    #parse attributes and methods
    for body_node in node.body:
        body_node_code = self.visit(body_node)
        if isinstance(body_node, ast.AnnAssign):    #body_node is an attribute
            self.tempAttributesDeclaretions[body_node.target.id]={'code':body_node_code,'type':self.visit(body_node.annotation)}
            #self.classDef_add_AnnAssign(body_node_code,body_node.target.id)
        elif not isinstance(body_node, ast.FunctionDef): #body_node is unsopported in class body
            raise ex.UnsupportedCommandError(node.body)

    if self.protected['methods'] == {} and self.private['methods'] == {} and self.public['methods'] == {} and not self.transplile_class:
        self.indent_level -= 1
        self.current_structure_name = None
        self.transplile_class = False
        return

        # check class is already defined
    if self.current_structure_name not in cppc.cppCodeObject.classes:  # class isn't already define
        cppc.cppCodeObject.classes[self.current_structure_name] = {}  # add class to scope
    else:  # class already define
        raise ex.AlreadyDefinedError(self.current_structure_name)

    #is not a constructor defined and there is one or more attribute, #FIXME always add constructor default for use istance of class in other class, is corrected?
    #if not (tm.(self.curcheck_callableFunctionrent_structure_name, '__init__','__init__')) and self.current_structure_name in tm.scope:  # FIXME correct __init__ with name of the class
    if len(self.protected['attributes']) != 0 or len(self.private['attributes']) != 0 or len(self.public['attributes']) != 0:
        constructor_code = ""
        if self.current_structure_name in self.current_structure_name:
            for var, type in tm.scope[self.current_structure_name].items():
                if not isinstance(type, dict):
                    default_value=tm.cppTypes_DefaultsValues.get(type)
                    if default_value is None:   #attribute contain istance of a class
                        default_value = ""
                    constructor_code += f"{var}({default_value}),"
            if constructor_code != "":  # class with parameters
                constructor_code = {
                    f"{self.indent()}{self.current_structure_name}()": f"{self.indent()}:{constructor_code.rstrip(',')} {{}}\n"}
                self.public['methods'] = {**constructor_code, **self.public['methods']}
    # operator method for debugging code
    code=""
    if self.current_structure_name in tm.scope:
        for var, type in tm.scope[self.current_structure_name].items():
            if not isinstance(type, dict):
                code += f'<<"{var}: "<<d.{var}<<","'

    if code !="":
        #remove last <,>@
        code = code[:-2] + code[-1:]
        #add method
        code_o = f'{self.indent()}{{\n'
        self.indent_level += 1
        code_o += f"{self.indent()}os{code};\n{self.indent()}return os;\n"
        self.indent_level-=1
        code_o+=f"{self.indent()}}}\n"
        self.public['methods'][f"{self.indent()}friend std::ostream & operator<<(std::ostream & os, const {self.current_structure_name} & d)"] = code_o

    #end of ClassDef node explorations
    if self.protected['attributes'] or self.protected['methods']:
        cppc.cppCodeObject.classes[self.current_structure_name]['protected']=self.protected
    if self.private['attributes'] or self.private['methods']:
        cppc.cppCodeObject.classes[self.current_structure_name]['private']=self.private
    if self.public['attributes'] or self.public['methods']:
        cppc.cppCodeObject.classes[self.current_structure_name]['public']=self.public

    self.indent_level -= 1
    self.current_structure_name=None
    self.transplile_class = False