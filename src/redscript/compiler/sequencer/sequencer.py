"""
Kinematic Sequencer: Transforms AST to Logical Graph
"""
from typing import Dict, List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from redscript.compiler.logical_graph import (
    LogicalGraph, Component, Connection, ComponentType, Port, SignalType, IDGenerator, Assertion as GraphAssertion
)
from redscript.compiler.parser.parser import (
    Program, Definition, Action, ControlFlow, ASTNode, Connection as ASTConnection, Assertion as ASTAssertion, ModuleDefinition,
    ForLoop, IfStatement, BinOp, PropertyAccess, Import, FromImport
)

class KinematicSequencer:
    """Transforms parsed AST into a logical graph of components"""
    
    def __init__(self):
        self.graph = LogicalGraph()
        self.component_map: Dict[str, str] = {}  # name -> component_id
        self.modules: Dict[str, ModuleDefinition] = {}
        self.scope_stack: List[str] = []
        self.variable_stack: List[Dict[str, any]] = [{}] # Stack of variable scopes

    
    def transform(self, ast: Program) -> LogicalGraph:
        """Transform AST to LogicalGraph"""
        IDGenerator.reset()
        for statement in ast.statements:
            self._process_statement(statement)
        
        return self.graph
    
    def _process_statement(self, statement: ASTNode) -> None:
        """Process a single statement"""
        if isinstance(statement, Definition):
            self._process_definition(statement)
        elif isinstance(statement, ModuleDefinition):
            self.modules[statement.name] = statement
        elif isinstance(statement, Action):
            self._process_action(statement)
        elif isinstance(statement, ControlFlow):
            self._process_control_flow(statement)
        elif isinstance(statement, ASTConnection):
            self._process_connection(statement)
        elif isinstance(statement, ASTAssertion):
            self._process_assertion(statement)
        elif isinstance(statement, ForLoop):
            self._process_for_loop(statement)
        elif isinstance(statement, IfStatement):
            self._process_if_statement(statement)
        elif isinstance(statement, Import):
            self._process_import(statement)
        elif isinstance(statement, FromImport):
            self._process_from_import(statement)
            
    def _process_import(self, stmt: Import) -> None:
        """Process an import statement"""
        import os
        from redscript.compiler.parser.parser import RedScriptParser
        
        # Resolve path
        # Assume relative to current working directory or needs a base path
        # For now, let's look relative to cwd and common include paths
        path = stmt.path
        if not os.path.exists(path):
            # Try examples/modules or similar if needed, or just fail
             if os.path.exists(os.path.join("examples", path)):
                 path = os.path.join("examples", path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Imported file not found: {stmt.path}")
            
        with open(path, 'r') as f:
            source = f.read()
            
        # Parse imported file
        parser = RedScriptParser()
        ast = parser.parse(source)
        
        # Process AST - we only care about ModuleDefinitions (and maybe Definitions if we want global components?)
        # For now, let's only allow loading Modules from imports to avoid side effects
        for statement in ast.statements:
            if isinstance(statement, ModuleDefinition):
                self.modules[statement.name] = statement
            elif isinstance(statement, Import):
                # Recursive import
                self._process_import(statement)

    def _process_from_import(self, stmt: FromImport) -> None:
        """Process a from...import statement with selective module loading"""
        import os
        from redscript.compiler.parser.parser import RedScriptParser
        
        # Resolve path (same logic as _process_import)
        path = stmt.path
        if not os.path.exists(path):
            if os.path.exists(os.path.join("examples", path)):
                path = os.path.join("examples", path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Imported file not found: {stmt.path}")
            
        with open(path, 'r') as f:
            source = f.read()
            
        # Parse imported file
        parser = RedScriptParser()
        ast = parser.parse(source)
        
        # Filter modules based on import specification
        for statement in ast.statements:
            if isinstance(statement, ModuleDefinition):
                # If importing all (*) or module is in the specified list
                if '*' in stmt.modules or statement.name in stmt.modules:
                    self.modules[statement.name] = statement
            elif isinstance(statement, Import):
                # Recursive import
                self._process_import(statement)
            elif isinstance(statement, FromImport):
                # Recursive from import
                self._process_from_import(statement)

    def _process_for_loop(self, loop: ForLoop) -> None:
        start = self._evaluate_expression(loop.start)
        end = self._evaluate_expression(loop.end)
        
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError(f"Loop range must evaluate to integers, got {start}, {end}")
            
        # Create new scope for loop variable
        self.variable_stack.append({})
        
        # Python range is exclusive at end, RedScript range might be inclusive?
        # Grammar: "range" "(" expr "," expr ")"
        # Usually range(0, 5) is 0..4. Let's stick to Python semantics for now.
        for i in range(start, end):
            self._set_variable(loop.variable, i)
            for stmt in loop.body:
                self._process_statement(stmt)
                
        self.variable_stack.pop()

    def _process_if_statement(self, stmt: IfStatement) -> None:
        condition = self._evaluate_expression(stmt.condition)
        
        if condition:
            for s in stmt.true_body:
                self._process_statement(s)
        elif stmt.false_body:
            for s in stmt.false_body:
                self._process_statement(s)

    def _evaluate_expression(self, expr):
        if isinstance(expr, int):
            return expr
        elif isinstance(expr, str):
            # Try variable first
            val = self._get_variable(expr)
            if val is not None:
                return val
            return expr 
        elif isinstance(expr, tuple):
            return tuple(self._evaluate_expression(e) for e in expr)
        elif isinstance(expr, list):
            return [self._evaluate_expression(e) for e in expr]
        elif isinstance(expr, dict):
            return {k: self._evaluate_expression(v) for k, v in expr.items()}
        elif isinstance(expr, BinOp):
            left = self._evaluate_expression(expr.left)
            right = self._evaluate_expression(expr.right)
            
            if expr.op == '+': return left + right
            elif expr.op == '-': return left - right
            elif expr.op == '*': return left * right
            elif expr.op == '/': return int(left / right)
            elif expr.op == '==': return left == right
            elif expr.op == '!=': return left != right
            elif expr.op == '<': return left < right
            elif expr.op == '>': return left > right
            elif expr.op == '<=': return left <= right
            elif expr.op == '>=': return left >= right
            elif expr.op == 'and': return left and right
            elif expr.op == 'or': return left or right
            else: raise ValueError(f"Unknown operator {expr.op}")
        return expr

    def _set_variable(self, name: str, value: any):
        self.variable_stack[-1][name] = value

    def _get_variable(self, name: str) -> any:
        for scope in reversed(self.variable_stack):
            if name in scope:
                return scope[name]
        return None

    
    def _process_definition(self, defn: Definition) -> None:
        """Process a component definition"""
        if defn.component_type in self.modules:
            self._instantiate_module(defn)
            return

        component_type = self._get_component_type(defn.component_type)
        
        # Evaluate parameters
        evaluated_params = {}
        for k, v in defn.parameters.items():
            evaluated_params[k] = self._evaluate_expression(v)
        
        component = Component(
            type=component_type,
            properties=evaluated_params
        )
        
        component_id = self.graph.add_component(component)
        full_name = self._get_scoped_name(defn.name)
        self.component_map[full_name] = component_id
    
    def _instantiate_module(self, defn: Definition) -> None:
        module = self.modules[defn.component_type]
        
        # Resolve arguments in outer scope
        resolved_args = {}
        for param_name, arg_value in defn.parameters.items():
            val = self._evaluate_expression(arg_value)
            # If it's a string, it might be a component ID (if resolved) or just a string value
            if isinstance(val, str):
                comp_id = self._resolve_name(val)
                if comp_id:
                    resolved_args[param_name] = comp_id
                else:
                    resolved_args[param_name] = val
            else:
                resolved_args[param_name] = val
        
        # Push scope
        self.scope_stack.append(defn.name)
        self.variable_stack.append({})
        
        # Register parameters in new scope
        for param_name, val in resolved_args.items():
            self._set_variable(param_name, val)
            
        # Process body
        for stmt in module.body:
            self._process_statement(stmt)
            
        self.variable_stack.pop()
        self.scope_stack.pop()

    def _get_scoped_name(self, name: str) -> str:
        if not self.scope_stack:
            return name
        return ".".join(self.scope_stack + [name])

    def _resolve_name(self, name: str) -> str:
        # Check variables first (for module parameters that are component IDs)
        val = self._get_variable(name)
        if val is not None and isinstance(val, str):
             return val

        # Try current scope
        full_name = self._get_scoped_name(name)
        if full_name in self.component_map:
            return self.component_map[full_name]
            
        # Walk up scopes
        parts = self.scope_stack[:]
        while parts:
            parts.pop()
            check_name = ".".join(parts + [name]) if parts else name
            if check_name in self.component_map:
                return self.component_map[check_name]
        
        return None

    def _process_action(self, action: Action) -> None:
        """Process an action (method call on component)"""
        component_id = self._resolve_name(action.component)
        if not component_id:
            raise ValueError(f"Component '{action.component}' not defined")
        
        # Evaluate arguments
        evaluated_args = [self._evaluate_expression(arg) for arg in action.arguments]
        
        # TODO: Implement action semantics (extend, retract, etc.)
    
    def _process_connection(self, conn: ASTConnection) -> None:
        """Process a signal connection (source -> target)"""
        source_comp_id = self._resolve_name(conn.source_component)
        target_comp_id = self._resolve_name(conn.target_component)
        
        if not source_comp_id:
            raise ValueError(f"Source component '{conn.source_component}' not defined")
        if not target_comp_id:
            raise ValueError(f"Target component '{conn.target_component}' not defined")
        
        # Get components
        source_comp = self.graph.components[source_comp_id]
        target_comp = self.graph.components[target_comp_id]
        
        # Get or create ports
        source_port = self._get_or_create_port(source_comp, conn.source_port, is_output=True)
        target_port = self._get_or_create_port(target_comp, conn.target_port, is_output=False)
        
        # Create connection
        connection = Connection(
            source_port_id=source_port.id,
            target_port_id=target_port.id,
            signal_strength=15,
            min_delay=0
        )
        self.graph.add_connection(connection)
    
    def _process_assertion(self, assertion: ASTAssertion) -> None:
        """Process a debug assertion"""
        comp_id = self._resolve_name(assertion.target)
        if not comp_id:
            raise ValueError(f"Assertion target '{assertion.target}' not defined")
        
        condition = f"{comp_id}.{assertion.property} == {assertion.value}"
        self.graph.add_assertion(GraphAssertion(condition=condition))

    def _get_or_create_port(self, component: Component, port_name: str, is_output: bool) -> Port:
        """Get an existing port or create a new one"""
        ports = component.outputs if is_output else component.inputs
        
        # Check existing ports
        for port in ports:
            if port.name == port_name:
                return port
        
        # Create new port
        port = Port(
            name=port_name,
            signal_type=SignalType.REDSTONE,
            strength=15
        )
        
        if is_output:
            component.outputs.append(port)
        else:
            component.inputs.append(port)
        
        return port
    
    def _process_control_flow(self, flow: ControlFlow) -> None:
        """Process control flow (parallel, sequence)"""
        for statement in flow.statements:
            self._process_statement(statement)
    
    def _get_component_type(self, type_str: str) -> ComponentType:
        """Map string to ComponentType"""
        type_map = {
            'Piston': ComponentType.PISTON,
            'StickyPiston': ComponentType.STICKY_PISTON,
            'Repeater': ComponentType.REPEATER,
            'Lever': ComponentType.LEVER,
            'Lamp': ComponentType.LAMP,
            'Observer': ComponentType.OBSERVER,
            'Dropper': ComponentType.DROPPER,
            'Door': ComponentType.PISTON,  # 3x3 door uses pistons
            'Comparator': ComponentType.COMPARATOR,
            'Hopper': ComponentType.HOPPER,
            'Target': ComponentType.TARGET,
            'SlimeBlock': ComponentType.SLIME_BLOCK,
            'HoneyBlock': ComponentType.HONEY_BLOCK,
            'RedstoneTorch': ComponentType.REDSTONE_TORCH,
            'PressurePlate': ComponentType.PRESSURE_PLATE,
            'Button': ComponentType.BUTTON,
            'Stone': ComponentType.STONE,
            'RedstoneWire': ComponentType.REDSTONE_WIRE,
            'GlazedTerracotta': ComponentType.GLAZED_TERRACOTTA,
            'Glass': ComponentType.GLASS,
            
            # Lowercase aliases
            'piston': ComponentType.PISTON,
            'sticky_piston': ComponentType.STICKY_PISTON,
            'repeater': ComponentType.REPEATER,
            'lever': ComponentType.LEVER,
            'lamp': ComponentType.LAMP,
            'observer': ComponentType.OBSERVER,
            'dropper': ComponentType.DROPPER,
            'comparator': ComponentType.COMPARATOR,
            'hopper': ComponentType.HOPPER,
            'target': ComponentType.TARGET,
            'slime_block': ComponentType.SLIME_BLOCK,
            'honey_block': ComponentType.HONEY_BLOCK,
            'redstone_torch': ComponentType.REDSTONE_TORCH,
            'pressure_plate': ComponentType.PRESSURE_PLATE,
            'button': ComponentType.BUTTON,
            'stone': ComponentType.STONE,
            'redstone_wire': ComponentType.REDSTONE_WIRE,
            'glazed_terracotta': ComponentType.GLAZED_TERRACOTTA,
            'glass': ComponentType.GLASS,
        }
        return type_map.get(type_str, ComponentType.PISTON)
