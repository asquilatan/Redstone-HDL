# Research: Advanced Debugging & Components

## 1. Debug Assertions & Manual State

**Problem**: Users need to verify circuit state and manually manipulate it during debugging.
**Solution**:
- **Grammar**: Add `assert` keyword and method call syntax (already exists).
- **Implementation**:
  - `assert(condition)`: Evaluated during simulation.
  - `block.setPosition(x,y,z)`: Updates `VoxelGrid` directly.
  - `block.setFacing(dir)`: Updates `properties`.

**Decision**: Implement `assert` as a statement and expose `VoxelGrid` manipulation methods to the interpreter.

## 2. Smart Redstone

**Problem**: Redstone wire doesn't visually connect to neighbors.
**Solution**:
- **Visuals**: In `VoxelRenderer`, check neighbors (N, S, E, W) for powerable components.
- **Logic**: `VoxelGrid` already handles connectivity via `RedstoneSimulator`.
- **Implementation**: Update `render_grid` to select correct texture/model (dot, line, cross) based on neighbors.

## 3. Custom Objects (Modules)

**Problem**: Users want to define reusable components (e.g., `DoublePistonExtender`).
**Solution**:
- **Grammar**: Add `module Name { ... }` syntax.
- **Instantiation**: `instance = Name(args)`.
- **Implementation**: Treat modules as macros that expand into the main graph.

## 4. Repeater Position Bug

**Problem**: Components appear in random positions.
**Solution**:
- **Cause**: `LogicalGraph` uses `uuid.uuid4()` for component IDs. The solver likely iterates over these IDs.
- **Fix**: Use deterministic IDs based on component name (e.g., `repeater_1`) or sequence index.

## 5. Debug Mode CLI

**Problem**: "See the entire schema after each iteration".
**Solution**:
- **CLI**: Add `--debug` flag.
- **Behavior**: Pause after each simulation tick or step, print state, allow user input (step, continue).
- **Naming**: `{block_type}.png`
- **Location**: `src/redscript/viewer/textures/`

**Required Textures**:
| File | Description |
|------|-------------|
| `stone.png` | Gray stone |
| `piston.png` | Piston face (wood + gray) |
| `sticky_piston.png` | Piston with green slime |
| `redstone_wire.png` | Red dust pattern |
| `repeater.png` | Repeater top view |
| `comparator.png` | Comparator top view |
| `lever.png` | Lever on stone |
| `lamp_off.png` | Brown lamp |
| `lamp_on.png` | Yellow glowing lamp |
| `button.png` | Stone button |
| `observer.png` | Observer face |
| `slime.png` | Green translucent |
| `honey.png` | Orange translucent |
| `target.png` | Red/white bullseye |
| `redstone_torch.png` | Red torch glow |

---

## 7. Block Info Display (NEW)

**Question**: How to show block information when looking at a block?

**Decision**: Extend raycast to include block type and properties in UI.

**Rationale**:
- Already have raycasting for coordinates
- Store `block_data` on entity for metadata
- Display: `Looking at: Repeater (delay=2) @ (5, 3, 10)`

---

## 8. Litematica Export (NEW)

**Question**: How to export to `.litematic` file?

**Decision**: Use `litemapy` library (already a dependency).

**Rationale**:
- Listed in `requirements.txt` and `setup.py`
- Direct API for creating Litematica schematics
- Already have `LitematicaSerializer` stub

**Implementation**:
```python
from litemapy import Schematic, Region, BlockState

def export_litematic(voxel_grid: VoxelGrid, path: str, name: str = "RedScript Export"):
    # Calculate bounds
    # Create Region with BlockStates
    # Save schematic
```

## 9. Advanced Control Flow & Materials (NEW)

**Decision**: Adopt C-style/Python-hybrid syntax for loops and conditionals.

**Rationale**:
- The existing language uses `{}` for blocks.
- `for i in range(start, end)` is familiar.
- `if (condition)` is standard.

**Proposed Grammar**:
```lark
for_loop: FOR_KW CNAME "in" range_expr "{" statement* "}"
range_expr: "range" "(" value "," value ")"
if_stmt: IF_KW "(" condition ")" "{" statement* "}" (ELSE_KW "{" statement* "}")?
FOR_KW: "for"
IF_KW: "if"
ELSE_KW: "else"
```

**Glass Block Behavior**:
- **Redstone Connectivity**: Redstone dust can be placed on top.
- **Diagonal Connectivity**: Does *not* cut redstone signals traveling diagonally.
- **Transparency**: Visually transparent.

**Parameterized Modules**:
- Extend `ModuleDefinition` to support variable substitution in parameters.
- Support simple arithmetic expressions (`+`, `-`, `*`, `/`) in values.


---

## Summary Table

| Component | Technology | Status |
|-----------|------------|--------|
| Block Interaction | Ursina `on_click` | Ready |
| Redstone Simulation | `RedstoneSimulator` class | Design complete |
| Block Textures | 16x16 PNG files | Need samples |
| Block Info Display | Extend raycast UI | Ready |
| Litematica Export | `litemapy` | Ready |

