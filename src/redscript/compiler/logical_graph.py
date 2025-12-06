"""
Logical Graph: Abstract representation of components and connections
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import uuid
from enum import Enum
from collections import defaultdict

class IDGenerator:
    """Generates deterministic IDs for components and connections"""
    _counters = defaultdict(int)

    @classmethod
    def generate(cls, prefix: str = "id") -> str:
        cls._counters[prefix] += 1
        return f"{prefix}_{cls._counters[prefix]}"
    
    @classmethod
    def reset(cls):
        cls._counters.clear()

class ComponentType(Enum):
    """Types of redstone components"""
    PISTON = "piston"
    STICKY_PISTON = "sticky_piston"
    REPEATER = "repeater"
    LEVER = "lever"
    LAMP = "lamp"
    OBSERVER = "observer"
    DROPPER = "dropper"
    COMPARATOR = "comparator"
    HOPPER = "hopper"
    TARGET = "target"
    SLIME_BLOCK = "slime_block"
    HONEY_BLOCK = "honey_block"
    REDSTONE_TORCH = "redstone_torch"
    PRESSURE_PLATE = "pressure_plate"
    BUTTON = "button"
    STONE = "stone"
    GLASS = "glass"
    REDSTONE_WIRE = "redstone_wire"
    GLAZED_TERRACOTTA = "glazed_terracotta"

class SignalType(Enum):
    """Types of signals"""
    REDSTONE = "redstone"
    MECHANICAL = "mechanical"

@dataclass
class Port:
    """A connection point on a component"""
    id: str = field(default_factory=lambda: IDGenerator.generate("port"))
    name: str = "default"
    component_id: str = ""
    offset: Tuple[int, int, int] = (0, 0, 0)  # Relative to component origin
    signal_type: SignalType = SignalType.REDSTONE
    is_input: bool = False
    strength: int = 15

@dataclass
class Component:
    """A logical unit (piston, repeater, etc.)"""
    id: str = field(default_factory=lambda: IDGenerator.generate("comp"))
    type: ComponentType = ComponentType.PISTON
    position: Tuple[int, int, int] = (0, 0, 0)  # World position
    dimensions: Tuple[int, int, int] = (1, 1, 1)
    properties: Dict[str, str] = field(default_factory=dict)
    inputs: List[Port] = field(default_factory=list)
    outputs: List[Port] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize default ports if not provided"""
        if not self.inputs:
            self.inputs = [Port(component_id=self.id, is_input=True)]
        if not self.outputs:
            self.outputs = [Port(component_id=self.id, is_input=False)]

@dataclass
class Connection:
    """A logical link between ports"""
    id: str = field(default_factory=lambda: IDGenerator.generate("conn"))
    source_port_id: str = ""
    target_port_id: str = ""
    min_delay: int = 0  # Ticks
    max_delay: int = 0
    signal_strength: int = 15

@dataclass
class Assertion:
    """A debug assertion"""
    condition: str
    message: str = "Assertion failed"

class LogicalGraph:
    """Graph of components and connections"""
    
    def __init__(self):
        self.components: Dict[str, Component] = {}
        self.connections: Dict[str, Connection] = {}
        self.assertions: List[Assertion] = []
    
    def add_assertion(self, assertion: Assertion) -> None:
        """Add a debug assertion"""
        self.assertions.append(assertion)
    
    def add_component(self, component: Component) -> str:
        """Add a component to the graph"""
        self.components[component.id] = component
        return component.id
    
    def get_component(self, component_id: str) -> Optional[Component]:
        """Retrieve a component"""
        return self.components.get(component_id)
    
    def add_connection(self, connection: Connection) -> str:
        """Add a connection between two ports"""
        self.connections[connection.id] = connection
        return connection.id
    
    def get_connections_for_component(self, component_id: str) -> List[Connection]:
        """Get all connections involving a component"""
        result = []
        for conn in self.connections.values():
            for port in self.components[component_id].inputs + self.components[component_id].outputs:
                if conn.source_port_id == port.id or conn.target_port_id == port.id:
                    result.append(conn)
        return result
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate the graph for logical consistency"""
        errors = []
        
        # Check for dangling connections
        for conn_id, conn in self.connections.items():
            port_found = False
            for comp in self.components.values():
                for port in comp.inputs + comp.outputs:
                    if port.id == conn.source_port_id or port.id == conn.target_port_id:
                        port_found = True
                        break
            if not port_found:
                errors.append(f"Connection {conn_id} references non-existent port")
        
        # Check for cycles (optional, depending on your semantics)
        # For now, we'll allow cycles (they could represent feedback loops)
        
        return len(errors) == 0, errors
