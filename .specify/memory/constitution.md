<!--
Sync Impact Report:
- Version change: 0.0.0 -> 1.0.0
- Modified principles: N/A (Initial Ratification)
- Added sections: All Principles, Governance
- Removed sections: N/A
- Templates requiring updates: plan-template.md (✅ updated), spec-template.md (✅ updated)
- Follow-up TODOs: None
-->

# Redstone HDL Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### Vanilla Survival Purity
<!-- Example: I. Library-First -->
All outputs must function without command blocks or admin tools. The system targets standard survival Minecraft mechanics exclusively.

### Physics-First Logic
<!-- Example: II. CLI Interface -->
Game mechanics like Quasi-Connectivity, Block Update Detection (BUD), and Sub-tick Update Order are treated as physical laws the compiler must simulate and respect to avoid failure. The compiler does not abstract away these mechanics but exposes them as constraints.

### Time as Semantics
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
The system must treat tick delays as functional data types equal to signal strength for exact synchronization. Timing is not a side effect; it is a first-class citizen in the language semantics.

### Spatial Isolation
<!-- Example: IV. Integration Testing -->
The auto-router must never create accidental cross-talk between adjacent wires. Signal integrity must be guaranteed by the layout engine through strict spacing or insulation blocks.

### Kinematic Safety
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
Generated machines must include internal pulse limiters preventing self-destruction. The system must verify that no generated circuit can destroy itself through piston interactions or other mechanical failures.

### Immediate Visual Verification
The system must provide a high-fidelity, interactive 3D preview of the generated structure independent of external tools so users can visually debug geometry before export. Visual feedback is critical for spatial debugging.

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution supersedes all other project practices.
Amendments require a documented RFC, approval by maintainers, and a migration plan for existing code.
All Pull Requests must verify compliance with these principles.
Complexity in implementation must be justified against these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
