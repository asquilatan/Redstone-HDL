import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from redscript.compiler.compiler import Compiler, CompileOptions

def test_selective_import():
    """Test importing specific modules"""
    source_code = """
    from "tests/multi_module_lib.rs" import Module1, Module3
    
    def m1 Module1(x=5)
    def m3 Module3(z=8)
    """
    
    compiler = Compiler()
    result = compiler.compile(source_code, CompileOptions(verbose=True))
    
    if result.success:
        print("[OK] Selective import compilation successful!")
        graph = result.schematic.logical_graph
        print(f"Components: {len(graph.components)}")
        
        # Expect 2 pistons (Module1 and Module3, NOT Module2)
        pistons = [c for c in graph.components.values() if c.type.value == 'piston']
        assert len(pistons) == 2, f"Expected 2 pistons, got {len(pistons)}"
        print("[OK] Verified only selected modules were imported.")
    else:
        print("[FAIL] Compilation failed:")
        for err in result.errors:
            print(f"  {err}")
        sys.exit(1)

def test_import_all():
    """Test importing all modules with *"""
    source_code = """
    from "tests/multi_module_lib.rs" import *
    
    def m1 Module1(x=1)
    def m2 Module2(y=2)
    def m3 Module3(z=3)
    """
    
    compiler = Compiler()
    result = compiler.compile(source_code, CompileOptions(verbose=True))
    
    if result.success:
        print("[OK] Import all (*) compilation successful!")
        graph = result.schematic.logical_graph
        print(f"Components: {len(graph.components)}")
        
        # Expect 3 pistons (all modules)
        pistons = [c for c in graph.components.values() if c.type.value == 'piston']
        assert len(pistons) == 3, f"Expected 3 pistons, got {len(pistons)}"
        print("[OK] Verified all modules were imported with *.")
    else:
        print("[FAIL] Compilation failed:")
        for err in result.errors:
            print(f"  {err}")
        sys.exit(1)

if __name__ == "__main__":
    print("=== Test 1: Selective Import ===")
    test_selective_import()
    print()
    print("=== Test 2: Import All (*) ===")
    test_import_all()
    print()
    print("[OK] All tests passed!")
