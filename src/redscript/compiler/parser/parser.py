"""
RedScript Parser: Converts source code to AST
"""
from lark import Lark, Transformer, Token
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from redscript.compiler.logical_graph import ComponentType

# Load grammar
GRAMMAR_PATH = Path(__file__).parent.parent / 'lexer' / 'grammar.lark'

class ASTNode:
    """Base class for AST nodes"""
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements if statements else []

class Definition(ASTNode):
    def __init__(self, name, component_type, parameters):
        self.name = name
        self.component_type = component_type
        self.parameters = parameters if parameters else {}

class Action(ASTNode):
    def __init__(self, component, method, arguments):
        self.component = component
        self.method = method
        self.arguments = arguments if arguments else []

class ControlFlow(ASTNode):
    def __init__(self, flow_type, statements):
        self.flow_type = flow_type
        self.statements = statements if statements else []

class Connection(ASTNode):
    def __init__(self, source_component, source_port, target_component, target_port):
        self.source_component = source_component
        self.source_port = source_port
        self.target_component = target_component
        self.target_port = target_port

class PortRef(ASTNode):
    def __init__(self, component, port):
        self.component = component
        self.port = port

class Assertion(ASTNode):
    def __init__(self, condition):
        self.condition = condition

class ModuleDefinition(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Import(ASTNode):
    def __init__(self, path):
        self.path = path

class FromImport(ASTNode):
    def __init__(self, path, modules):
        self.path = path
        self.modules = modules  # List of module names or ['*'] for all

class ForLoop(ASTNode):
    def __init__(self, variable, start, end, body):
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body

class IfStatement(ASTNode):
    def __init__(self, condition, true_body, false_body=None):
        self.condition = condition
        self.true_body = true_body
        self.false_body = false_body

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class PropertyAccess(ASTNode):
    def __init__(self, component, property):
        self.component = component
        self.property = property

class RedScriptTransformer(Transformer):
    """Transforms Lark tree to AST"""
    
    def program(self, items):
        statements = [s for s in items if isinstance(s, (Definition, Action, ControlFlow, Connection, Assertion, ModuleDefinition, ForLoop, IfStatement, Import, FromImport))]
        return Program(statements)
    
    def import_stmt(self, items):
        return Import(str(items[1]))
    
    def from_import(self, items):
        # items: [FROM_KW, STRING, IMPORT_KW, (STAR | module_list)]
        path = str(items[1])
        if isinstance(items[3], str) and items[3] == '*':
            modules = ['*']
        else:
            modules = items[3]  # module_list
        return FromImport(path, modules)
    
    def module_list(self, items):
        return [str(item) for item in items]
    
    def module_def(self, items):
        # items: [MODULE_KW, CNAME, param_list?, block]
        name = str(items[1])
        params = []
        body = []
        
        if len(items) == 4:
            params = items[2]
            body = items[3]
        else:
            body = items[2]
                
        return ModuleDefinition(name, params, body)

    def block(self, items):
        return [s for s in items if isinstance(s, (Definition, Action, ControlFlow, Connection, Assertion, ModuleDefinition, ForLoop, IfStatement, Import, FromImport))]

    def control_flow(self, items):
        if isinstance(items[0], (ForLoop, IfStatement)):
            return items[0]
            
        flow_type = str(items[0])
        if flow_type == "wait":
            return ControlFlow(flow_type, [int(items[1])]) # items: [WAIT_KW, NUMBER]
            
        statements = items[1] # items: [FLOW_KW, block]
        return ControlFlow(flow_type, statements)

    def for_loop(self, items):
        # items: [FOR_KW, CNAME, range_expr, block]
        variable = str(items[1])
        start, end = items[2]
        body = items[3]
        return ForLoop(variable, start, end, body)

    def range_expr(self, items):
        # items: [expr, expr]
        return (items[0], items[1])

    def if_stmt(self, items):
        # items: [IF_KW, bool_expr, block, (ELSE_KW, block)?]
        condition = items[1]
        true_body = items[2]
        false_body = None
        if len(items) > 3:
            false_body = items[4] # items[3] is ELSE_KW
        return IfStatement(condition, true_body, false_body)

    def eq(self, items): return BinOp(items[0], '==', items[1])
    def neq(self, items): return BinOp(items[0], '!=', items[1])
    def lt(self, items): return BinOp(items[0], '<', items[1])
    def gt(self, items): return BinOp(items[0], '>', items[1])
    def le(self, items): return BinOp(items[0], '<=', items[1])
    def ge(self, items): return BinOp(items[0], '>=', items[1])

    def add(self, items): return BinOp(items[0], '+', items[1])
    def sub(self, items): return BinOp(items[0], '-', items[1])
    def mul(self, items): return BinOp(items[0], '*', items[1])
    def div(self, items): return BinOp(items[0], '/', items[1])

    def property_access(self, items):
        return PropertyAccess(str(items[0]), str(items[1]))

    def param_list(self, items):
        return [str(i) for i in items]

    def definition(self, items):
        # items: [DEF_KW, CNAME, type_name, parameters?]
        name = str(items[1])
        component_type = str(items[2])
        parameters = {}
        
        if len(items) > 3:
            parameters = items[3]
            
        return Definition(name, component_type, parameters)
    
    def type_name(self, items):
        return str(items[0])

    def parameters(self, items):
        result = {}
        for item in items:
            if isinstance(item, tuple) and len(item) == 2:
                result[item[0]] = item[1]
        return result
    
    def parameter(self, items):
        key = str(items[0])
        value = items[1]
        return (key, value)
    
    def action(self, items):
        # items: [CNAME, CNAME, arguments?]
        component = str(items[0])
        method = str(items[1])
        arguments = []
        if len(items) > 2:
            arguments = items[2]
        return Action(component, method, arguments)
    
    def arguments(self, items):
        return list(items)
    
    def argument(self, items):
        if len(items) == 2:  # Key-value pair: CNAME, expression
            return {str(items[0]): items[1]}
        else:  # Positional argument: expression
            return items[0]
    
    def tuple(self, items):
        # items: [e1, e2, e3]
        return (items[0], items[1], items[2])
    
    def assertion(self, items):
        # items: [ASSERT_KW, bool_expr]
        return Assertion(items[1])

    def connection(self, items):
        # items: [port_ref, port_ref]
        source = items[0]
        target = items[1]
        return Connection(source.component, source.port, target.component, target.port)
    
    def port_ref(self, items):
        # items: [CNAME, CNAME]
        return PortRef(str(items[0]), str(items[1]))
    
    def CNAME(self, token):
        return str(token)
    
    def COMPONENT_TYPE(self, token):
        return str(token)
    
    def PARALLEL_KW(self, token):
        return "parallel"
    
    def SEQUENCE_KW(self, token):
        return "sequence"
    
    def WAIT_KW(self, token):
        return "wait"
    
    def STAR(self, token):
        return "*"
    
    def STRING(self, token):
        return str(token)[1:-1]  # Remove quotes
    
    def NUMBER(self, token):
        return int(token)

class RedScriptParser:
    """Parser for RedScript language"""
    
    def __init__(self):
        # Read grammar from file
        with open(GRAMMAR_PATH, 'r') as f:
            grammar = f.read()
        self.parser = Lark(grammar, parser='lalr', transformer=RedScriptTransformer())
    
    def parse(self, source_code: str) -> Program:
        """Parse source code to AST"""
        try:
            result = self.parser.parse(source_code)
            return result
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise SyntaxError(f"Parse error: {e}")
