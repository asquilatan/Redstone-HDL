# Feature Specification: Advanced Debugging & Components

## 1. Overview
This feature introduces advanced debugging capabilities, including assertions, manual state manipulation, and a step-by-step debug mode. It also enhances the visual fidelity of redstone dust ("smart redstone"), adds support for reusable custom modules, and fixes non-deterministic component positioning.

## 2. Functional Requirements

### 2.1 Debugging System
- **Assertions**:
  - Syntax: `assert(condition)`
  - Behavior: Evaluated during simulation. If false, simulation pauses/halts with error.
  - Conditions: Check block state (powered, position, properties).
- **Manual State Manipulation**:
  - Ability to modify block state during debug session.
  - Methods: `setPosition(x, y, z)`, `setFacing(direction)`, `toggle()`.
- **Debug Mode CLI**:
  - Flag: `--debug`
  - Features:
    - Step-by-step simulation (tick by tick).
    - Inspect current state of components.
    - Execute manual state commands.

### 2.2 Smart Redstone Rendering
- **Visuals**: Redstone dust should visually connect to adjacent power sources and other dust.
- **Logic**: Use neighbor checking in `VoxelRenderer` to select the correct texture/model (dot, line, corner, T-junction, cross).

### 2.3 Custom Modules
- **Definition**: Define reusable sub-circuits.
  - Syntax: `module Name { ... }`
- **Instantiation**: Use modules as components.
  - Syntax: `instance = Name(args)`
- **Expansion**: Compiler expands modules into the main logical graph.

### 2.4 Bug Fixes
- **Repeater Positioning**: Ensure repeaters and other components have deterministic positions/IDs across compilations.

## 3. Technical Requirements
- **Grammar**: Update `grammar.lark` for `assert` and `module`.
- **Compiler**:
  - Implement `ModuleDefinition` and `ModuleInstance` in AST.
  - Implement module expansion phase.
  - Update `IDGenerator` for deterministic IDs.
- **Simulator**:
  - Integrate `Assertion` checking.
  - Expose API for manual state changes.
- **Viewer**:
  - Update `render_grid` for smart redstone texture selection.

## 4. User Stories (Prioritized)

- **US1 (P1) - Debug Mode & Assertions**: As a user, I want to pause simulation and verify state so I can find logic errors.
- **US2 (P1) - Smart Redstone**: As a user, I want redstone dust to look connected so I can visually verify the circuit path.
- **US3 (P2) - Custom Modules**: As a user, I want to define reusable modules so I can build complex circuits without repetition.
- **US4 (P3) - Manual State Control**: As a user, I want to manually toggle levers or move blocks in debug mode to test specific scenarios.
- **US5 (P0) - Deterministic Builds**: As a user, I want my components to stay in the same place when I recompile so I don't lose my bearings.


