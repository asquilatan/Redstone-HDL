# Feature Specification: RedScript Compiler

**Feature Branch**: `001-redscript-compiler`
**Created**: 2025-12-06
**Status**: Draft
**Input**: User description: "Define the functional requirements for "RedScript," a hardware description language and compiler that translates high-level kinematic intent (e.g., "Open 3x3 Door", "Move Block to X") into optimized 3D voxel schematics by decoupling logic from physical wiring. The specification must feature a "Kinematic Sequencer" that abstracts complex motion primitives like double-piston extenders into single commands, a "3D Auto-Router" capable of pathfinding redstone dust and glass towers through complex geometry while avoiding signal interference, a "Timing Engine" that automatically inserts repeaters to synchronize parallel actions, and a "Live Voxel Viewer" that renders the compiled machine in a simple 3D environment, allowing the user to rotate, zoom, and inspect internal wiring layers to verify block placements before committing to a Litematica export."

## Constitution Compliance

- **Vanilla Survival Purity**: Confirmed. The compiler generates standard blocks (pistons, dust, repeaters) usable in vanilla survival without command blocks.
- **Physics-First Logic**: The Kinematic Sequencer and Timing Engine explicitly model Quasi-Connectivity, BUDs, and sub-tick update orders to ensure reliability.
- **Time as Semantics**: The Timing Engine treats tick delays as a functional data type, inserting repeaters to enforce exact synchronization defined in the script.
- **Spatial Isolation**: The 3D Auto-Router guarantees signal integrity by maintaining spacing or placing insulation blocks to prevent cross-talk.
- **Kinematic Safety**: The compiler includes a verification pass to insert pulse limiters and prevent piston configurations that would cause self-destruction.
- **Immediate Visual Verification**: The Live Voxel Viewer provides an interactive 3D preview for inspection before export.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Define Kinematic Intent (Priority: P1)

Users can write high-level RedScript code to define mechanical actions (e.g., `piston.extend()`) without manually placing blocks.

**Why this priority**: This is the core value proposition—decoupling logic from physical wiring. Without this, it's just a CAD tool.

**Independent Test**: Create a RedScript file with a single piston action. Compile it. Verify the output schematic contains a piston and a power source connected to it.

**Acceptance Scenarios**:

1. **Given** a RedScript file with `Door.open()`, **When** the compiler runs, **Then** it generates a schematic with the correct piston layout for a door.
2. **Given** a script with `Block.move(to: X)`, **When** compiled, **Then** the output contains a piston feed tape or flying machine to move the block.

---

### User Story 2 - Auto-Route Wiring (Priority: P1)

The system automatically routes redstone dust and glass towers between logical components, avoiding obstacles.

**Why this priority**: Manual wiring is the most tedious and error-prone part of Redstone engineering. Automation here is essential for the "Compiler" aspect.

**Independent Test**: Place two logical components (input lever, output lamp) at a distance in the script. Compile. Verify they are connected by a valid redstone line in the schematic.

**Acceptance Scenarios**:

1. **Given** an input and output separated by complex geometry, **When** the Auto-Router runs, **Then** it finds a valid path for the redstone signal.
2. **Given** two parallel signal lines, **When** routed, **Then** they are spaced or insulated to prevent cross-talk.

---

### User Story 3 - Synchronize Actions (Priority: P2)

The Timing Engine automatically inserts repeaters to ensure parallel actions happen in the correct tick order.

**Why this priority**: Complex machines (like 3x3 doors) fail if timing is off by even 1 tick. Manual tuning is difficult; automation ensures reliability.

**Independent Test**: Define two actions, one instant and one delayed by 4 ticks. Compile. Verify the instant action's line has a 4-tick repeater delay added to match the other (or vice versa depending on intent).

**Acceptance Scenarios**:

1. **Given** a double-piston extender sequence, **When** compiled, **Then** the repeaters are set to the exact ticks required for the extend/retract physics.
2. **Given** multiple parallel pistons moving a slime block structure, **When** compiled, **Then** they fire in the exact same tick to prevent breakage.

---

### User Story 4 - Visual Inspection (Priority: P2)

Users can view the generated structure in a 3D Live Voxel Viewer to inspect wiring and placement.

**Why this priority**: "Immediate Visual Verification" is a constitutional requirement. Users need to trust the compiler before building.

**Independent Test**: Compile a design and launch the viewer. Verify the structure is rendered and the camera can rotate around it.

**Acceptance Scenarios**:

1. **Given** a compiled schematic, **When** the viewer is launched, **Then** the user sees the 3D model.
2. **Given** a complex internal mechanism, **When** the user zooms in and hides outer layers, **Then** the internal wiring is visible.

---

### User Story 5 - Export to Litematica (Priority: P3)

Users can export the final design to a `.litematic` file for use in Minecraft.

**Why this priority**: Connects the tool to the actual game. P3 because the viewer (P2) allows validation first, but export is the final goal.

**Independent Test**: Export a simple design. Load it into Litematica in Minecraft. Verify it loads correctly.

**Acceptance Scenarios**:

1. **Given** a verified design, **When** exported, **Then** a valid `.litematic` file is created.
2. **Given** the exported file, **When** pasted in Minecraft, **Then** the blocks match the design.

### Edge Cases

- What happens when the Auto-Router cannot find a path? (Should error with "Routing Failed" and highlight the obstruction).
- How does system handle conflicting timing constraints? (Should report a "Timing Violation" error).
- What happens if the generated structure exceeds Minecraft's build height? (Should warn or error).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST parse RedScript source code into an Abstract Syntax Tree (AST).
- **FR-002**: The Kinematic Sequencer MUST transform AST nodes into a logical graph of block components (pistons, observers, etc.).
- **FR-003**: The 3D Auto-Router MUST generate a voxel grid with valid redstone wiring connecting the logical graph.
- **FR-004**: The Auto-Router MUST enforce "Spatial Isolation" by maintaining at least 1 air block or placing solid insulation blocks between distinct signal lines.
- **FR-005**: The Timing Engine MUST calculate signal propagation delay and insert repeaters to match the user-defined or physics-required timing.
- **FR-006**: The system MUST perform a "Kinematic Safety" check to detect and prevent self-destructing configurations (e.g., pistons pushing immovable blocks).
- **FR-007**: The Live Voxel Viewer MUST render the voxel grid in a window using a 3D graphics library.
- **FR-008**: The Live Voxel Viewer MUST provide controls for camera rotation, panning, and zooming.
- **FR-009**: The system MUST serialize the final voxel grid into the Litematica file format (`.litematic`).
- **FR-010**: The compiler MUST support "Physics-First" constraints, exposing QC and BUD properties as edge cases in the routing graph.

### Key Entities

- **Script**: The user-written code file (`.rs`).
- **LogicalGraph**: The abstract representation of components and connections.
- **VoxelGrid**: The 3D array of blocks representing the physical machine.
- **SignalPath**: A route taken by redstone power, including delay and strength attributes.
- **Schematic**: The binary output file.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can compile a standard "3x3 Piston Door" script into a working schematic in under 5 seconds.
- **SC-002**: The Auto-Router successfully connects 95% of valid logical graphs without user intervention.
- **SC-003**: 100% of generated schematics pass the internal "Kinematic Safety" check before export.
- **SC-004**: The Live Voxel Viewer renders a 10,000-block structure at >30 FPS on standard hardware.
- **SC-005**: Exported `.litematic` files load in Minecraft Litematica mod version 1.20+ without errors.
