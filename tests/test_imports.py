import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from redscript.compiler.compiler import Compiler, CompileOptions

def test_imports():
    # Path to the main script
    script_path = "tests/test_import_script.rs"
    
    with open(script_path, 'r') as f:
        source = f.read()

    compiler = Compiler()
    # We might need to handle CWD for relative imports. 
    # processing is in sequencer, which uses os.path.join(cwd, path) or similar logic
    
    result = compiler.compile(source, CompileOptions(verbose=True))
    
    if result.success:
        print("Compilation successful!")
        graph = result.schematic.logical_graph
        print(f"Components: {len(graph.components)}")
        
        # Expect 1 piston
        pistons = [c for c in graph.components.values() if c.type.value == 'piston']
        assert len(pistons) == 1
        print("Verified imported module was instantiated.")
        
    else:
        print("Compilation failed:")
        for err in result.errors:
            print(f"  {err}")
        sys.exit(1)

if __name__ == "__main__":
    test_imports()
