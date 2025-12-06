import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from redscript.compiler.compiler import Compiler, CompileOptions

def test_advanced_features():
    source_code = """
    module PistonColumn(height, x_pos) {
        for i in range(0, height) {
            def p piston(
                pos=(x_pos, i, 0),
                facing="up"
            )
            
            if (i > 2) {
                def g glass(pos=(x_pos + 1, i, 0))
            } else {
                def s stone(pos=(x_pos + 1, i, 0))
            }
        }
    }

    def col1 PistonColumn(height=5, x_pos=0)
    """
    
    compiler = Compiler()
    result = compiler.compile(source_code, CompileOptions(verbose=True))
    
    if result.success:
        print("Compilation successful!")
        # Verify graph content
        graph = result.schematic.logical_graph
        print(f"Components: {len(graph.components)}")
        for cid, comp in graph.components.items():
            print(f"  {cid}: {comp.type} {comp.properties}")
            
        # Expected: 5 pistons, 3 stones (0,1,2), 2 glass (3,4)
        # Total 10 components
        
        pistons = [c for c in graph.components.values() if c.type.value == 'piston']
        stones = [c for c in graph.components.values() if c.type.value == 'stone']
        glass = [c for c in graph.components.values() if c.type.value == 'glass']
        
        print(f"Pistons: {len(pistons)}")
        print(f"Stones: {len(stones)}")
        print(f"Glass: {len(glass)}")
        
        assert len(pistons) == 5
        assert len(stones) == 3
        assert len(glass) == 2

        # Verify positions in VoxelGrid
        grid = result.schematic.voxel_grid
        # Piston at 0,0,0
        assert grid.get_block(0, 0, 0) is not None
        assert grid.get_block(0, 0, 0).material == "minecraft:piston"
        
        # Piston at 0,4,0 
        assert grid.get_block(0, 4, 0) is not None
        assert grid.get_block(0, 4, 0).material == "minecraft:piston"

        # Stone at 1,0,0
        assert grid.get_block(1, 0, 0) is not None
        assert grid.get_block(1, 0, 0).material == "minecraft:stone"

        # Glass at 1,3,0
        assert grid.get_block(1, 3, 0) is not None
        assert grid.get_block(1, 3, 0).material == "minecraft:glass"
        
    else:
        print("Compilation failed:")
        for err in result.errors:
            print(f"  {err}")
        sys.exit(1)

if __name__ == "__main__":
    test_advanced_features()
