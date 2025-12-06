# Redstone_HDL Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-06

## Active Technologies
- Python 3.13 + Lark (Parsing), Ursina (Viewer/3D), Pytest (Testing) (main)
- File-based (.rs source, .litematic output) (main)
- Python 3.11+ + Ursina 5.0+, litemapy 0.4+, Pillow (for textures) (main)
- File-based (PNG textures, .litematic exports) (main)
- [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION] + [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION] (main)
- [if applicable, e.g., PostgreSQL, CoreData, files or N/A] (main)
- Python 3.13 + Ursina (Viewer), Lark (Grammar), NetworkX (Graph) (main)
- Files (.rs source, .litematic export) (main)
- Python 3.13 + Lark (Parsing), Ursina (Rendering) (main)
- Files (.rs, .litematic) (main)

- Python 3.11+ + Lark, Ursina, Pybind11 (001-redscript-compiler)
- C++ (Pathfinding Extensions)

## Project Structure

```text
src/
├── redscript/
│   ├── compiler/
│   ├── solver/
│   ├── viewer/
│   └── cli/
└── cpp/
tests/
```

## Commands

pip install .; pytest; tox

## Code Style

Python: PEP 8, Type Hints
C++: Google Style Guide

## Recent Changes
- main: Added Python 3.13 + Lark (Parsing), Ursina (Rendering)
- main: Added Python 3.13 + Lark (Parsing), Ursina (Rendering)
- main: Added [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION] + [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
