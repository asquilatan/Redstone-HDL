# Tasks: Advanced Debugging & Components

**Input**: Design documents from `/specs/main/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/debug_api.yaml ✓

**Tests**: Not explicitly requested - tests excluded unless noted.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- Paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare environment for new features

- [ ] T001 [P] Create redstone_wire_dot.png in src/redscript/viewer/textures/
- [ ] T002 [P] Create redstone_wire_line.png in src/redscript/viewer/textures/
- [ ] T003 [P] Create redstone_wire_corner.png in src/redscript/viewer/textures/
- [ ] T004 [P] Create redstone_wire_t.png in src/redscript/viewer/textures/
- [ ] T005 [P] Create redstone_wire_cross.png in src/redscript/viewer/textures/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required by all user stories
**Priority**: P0 (Critical Fix)

- [ ] T006 [US5] Implement IDGenerator class in src/redscript/compiler/sequencer/sequencer.py
- [ ] T007 [US5] Replace uuid.uuid4() with IDGenerator in LogicalGraph (src/redscript/compiler/logical_graph.py)
- [ ] T008 [US5] Update KinematicSequencer to use IDGenerator in src/redscript/compiler/sequencer/sequencer.py

**Checkpoint**: Compilation is deterministic - User Story 5 complete

---

## Phase 3: User Story 1 - Debug Mode & Assertions (Priority: P1)

**Goal**: Pause simulation, verify state, and step through execution

**Independent Test**: Run `redscript compile test.rs --debug`, step through ticks, verify assertions fail/pass

### Implementation for User Story 1

- [x] T009 [US1] Update grammar.lark to support `assert` statement in src/redscript/compiler/lexer/grammar.lark
- [x] T010 [US1] Add Assertion dataclass to src/redscript/compiler/compiler.py
- [x] T011 [US1] Implement Assertion parsing in RedScriptParser (src/redscript/compiler/parser/parser.py)
- [x] T012 [US1] Create DebugContext class in src/redscript/viewer/simulator.py
- [x] T013 [US1] Implement step-by-step simulation loop in RedstoneSimulator (src/redscript/viewer/simulator.py)
- [x] T014 [US1] Add `--debug` flag to CLI in src/redscript/cli/main.py
- [x] T015 [US1] Implement interactive debug shell in src/redscript/cli/main.py

**Checkpoint**: Debug mode working - User Story 1 complete

---

## Phase 4: User Story 2 - Smart Redstone (Priority: P1)

**Goal**: Redstone dust visually connects to neighbors

**Independent Test**: View a circuit, confirm redstone wires form lines/corners instead of isolated dots

### Implementation for User Story 2

- [x] T016 [US2] Implement neighbor connection logic in VoxelRenderer.render_grid (src/redscript/viewer/renderer.py)
- [x] T017 [US2] Update texture selection based on connections in src/redscript/viewer/renderer.py

**Checkpoint**: Redstone looks connected - User Story 2 complete

---

## Phase 5: User Story 3 - Custom Modules (Priority: P2)

**Goal**: Define and reuse sub-circuits

**Independent Test**: Compile a file with `module` definition and usage, verify correct expansion

### Implementation for User Story 3

- [x] T018 [US3] Update grammar.lark to support `module` definition and instantiation in src/redscript/compiler/lexer/grammar.lark
- [x] T019 [US3] Add ModuleDefinition and ModuleInstance to AST in src/redscript/compiler/parser/parser.py
- [x] T020 [US3] Implement module expansion pass in Compiler (src/redscript/compiler/compiler.py)
- [x] T021 [US3] Create test case for module usage in examples/module_test.rs

**Checkpoint**: Modules working - User Story 3 complete

---

## Phase 6: User Story 4 - Manual State Control (Priority: P3)

**Goal**: Manually manipulate block state during debug

**Independent Test**: In debug mode, use `setPosition` or `toggle` and see effect in viewer/simulation

### Implementation for User Story 4

- [x] T022 [US4] Implement `toggle` command in debug shell (src/redscript/cli/debug.py)
- [x] T023 [US4] Implement `set` command in debug shell (src/redscript/cli/debug.py)

**Checkpoint**: Manual control working - User Story 4 complete

## Completion

All phases completed. The system now supports:
1. Deterministic compilation (IDGenerator)
2. Debug assertions (`assert`)
3. Interactive debugger (`--debug`)
4. Smart redstone rendering (connected textures)
5. Custom modules (`module`)
6. Manual state control (`toggle`, `set`)

### Implementation for User Story 4

- [ ] T022 [US4] Implement setPosition/setFacing methods in RedstoneSimulator (src/redscript/viewer/simulator.py)
- [ ] T023 [US4] Expose manual state commands to Debug CLI (src/redscript/cli/main.py)
- [ ] T024 [US4] Update VoxelGrid from Simulator state changes (src/redscript/compiler/voxel_grid.py)

**Checkpoint**: Manual control working - User Story 4 complete

---

## Phase 7: User Story 6 - Advanced Control Flow & Materials (Priority: P2)

**Goal**: Loops, conditionals, glass blocks, and parameterized modules

**Independent Test**: Compile `examples/advanced_features.rs` containing loops, if-statements, and glass.

### Implementation for User Story 6

- [x] T027 [US6] Update grammar.lark for `for`, `if`, `Glass`, and expressions in src/redscript/compiler/lexer/grammar.lark
- [x] T028 [US6] Add ForLoop and IfStatement AST nodes in src/redscript/compiler/parser/parser.py
- [x] T029 [US6] Implement expression evaluation logic in src/redscript/compiler/sequencer/sequencer.py
- [x] T030 [US6] Implement loop unrolling and conditional execution in KinematicSequencer (src/redscript/compiler/sequencer/sequencer.py)
- [x] T031 [US6] Update module instantiation to support parameterized expressions in src/redscript/compiler/sequencer/sequencer.py
- [x] T032 [US6] Add Glass component type to src/redscript/compiler/logical_graph.py
- [x] T033 [US6] Implement Glass rendering with transparency in src/redscript/viewer/renderer.py
- [x] T034 [US6] Create demonstration file examples/advanced_features.rs

**Checkpoint**: Advanced features working - User Story 6 complete

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and final cleanup

- [ ] T035 [P] Update README.md with Debug Mode and Advanced Feature instructions
- [ ] T036 [P] Verify all examples work with new ID generation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Independent
- **Foundational (Phase 2)**: Critical for all subsequent phases (US5)
- **User Stories (Phases 3-7)**:
  - US1 (Debug) depends on Foundational
  - US2 (Smart Redstone) depends on Foundational
  - US3 (Modules) depends on Foundational
  - US4 (Manual State) depends on US1
  - US6 (Advanced Features) depends on US3 (for parameterized modules)

### Parallel Opportunities

- US2 (Smart Redstone) can run parallel to US1/US3
- US3 (Modules) can run parallel to US1/US2
- US6 (Advanced Features) can run parallel to US4

---

## Implementation Strategy

### MVP First (US5 + US1)

1. Fix deterministic IDs (US5) - **CRITICAL**
2. Implement Debug Mode (US1) - **CORE FEATURE**
3. Validate with simple circuit

### Incremental Delivery

1. US5 (Fixes)
2. US1 (Debug)
3. US2 (Visuals)
4. US3 (Modules)
5. US4 (Manual Control)
6. US6 (Advanced Features)

**Total**: 36 tasks
**MVP Scope**: T006-T015 (10 tasks)

**Purpose**: Documentation and final cleanup

- [ ] T025 [P] Update README.md with Debug Mode instructions
- [ ] T026 [P] Verify all examples work with new ID generation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Independent
- **Foundational (Phase 2)**: Critical for all subsequent phases (US5)
- **User Stories (Phases 3-6)**:
  - US1 (Debug) depends on Foundational
  - US2 (Smart Redstone) depends on Foundational (uses VoxelGrid)
  - US3 (Modules) depends on Foundational (Compiler changes)
  - US4 (Manual State) depends on US1 (Debug CLI)

### Parallel Opportunities

- Texture creation (T001-T005)
- US2 (Smart Redstone) can run parallel to US1/US3
- US3 (Modules) can run parallel to US1/US2

---

## Implementation Strategy

### MVP First (US5 + US1)

1. Fix deterministic IDs (US5) - **CRITICAL**
2. Implement Debug Mode (US1) - **CORE FEATURE**
3. Validate with simple circuit

### Incremental Delivery

1. US5 (Fixes)
2. US1 (Debug)
3. US2 (Visuals)
4. US3 (Modules)
5. US4 (Manual Control)

**Total**: 26 tasks
**MVP Scope**: T006-T015 (10 tasks)
