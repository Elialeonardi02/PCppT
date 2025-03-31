from enum import Enum
import ast
from pcppt import exceptions as ex, typesMapping as tm, codeCppClass as cppc
from DSL.operators import FOperatorKind

def visit_ClassDef(self, node):  # visit e translate in C++ ClassDef node
    if self.operator==FOperatorKind.NONE:
        raise ex.UnsupportedCommandError("unrecognized operator")
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