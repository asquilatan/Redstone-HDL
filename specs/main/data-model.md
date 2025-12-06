# Data Model: Advanced Debugging & Components

## 1. Logical Graph Extensions

### 1.1 Module Definition
Represents a reusable component definition.
```python
@dataclass
class ModuleDefinition:
    name: str
    parameters: List[str]
    body: List[ASTNode]
```

### 1.2 Module Instance
Represents a usage of a module.
```python
@dataclass
class ModuleInstance(Component):
    module_name: str
    arguments: Dict[str, Any]
```

## 2. Debugging System

### 2.1 Assertion
Represents a verification step in the simulation.
```python
@dataclass
class Assertion:
    target: str  # Component ID or name
    property: str # e.g., "powered", "position"
    expected_value: Any
    tick: int # Simulation tick to check
```

### 2.2 Debug Context
Stores the state of the debugging session.
```python
@dataclass
class DebugContext:
    breakpoints: Set[int] # Ticks to pause at
    current_tick: int
    history: List[Dict[str, Any]] # State history for time travel/inspection
```

## 3. Compiler Extensions

### 3.1 Deterministic ID Generation
Replace `uuid.uuid4()` with a deterministic generator.
```python
class IDGenerator:
    def __init__(self):
        self.counters = defaultdict(int)
    
    def generate(self, prefix: str) -> str:
        self.counters[prefix] += 1
        return f"{prefix}_{self.counters[prefix]}"
```

## 4. Control Flow Extensions (NEW)

### 4.1 For Loop
Represents a compile-time loop.
```python
@dataclass
class ForLoop(ASTNode):
    variable: str
    start: int
    end: int
    body: List[ASTNode]
```

### 4.2 If Statement
Represents a compile-time conditional.
```python
@dataclass
class IfStatement(ASTNode):
    condition: str # Expression string
    true_body: List[ASTNode]
    false_body: List[ASTNode]
```

### 4.3 Glass Component
New component type for semi-solid blocks.
```python
class ComponentType(Enum):
    # ... existing types ...
    GLASS = "glass"
```

