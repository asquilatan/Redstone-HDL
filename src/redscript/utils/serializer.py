"""
Litematica Serializer: Export voxel grids to .litematic format
"""
import sys
from pathlib import Path
from typing import Dict, Tuple, Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from redscript.compiler.voxel_grid import VoxelGrid

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from litemapy import Region, BlockState
    LITEMAPY_AVAILABLE = True
except ImportError:
    LITEMAPY_AVAILABLE = False
    BlockState = None

@dataclass
class LitematicaMetadata:
    """Metadata for exported schematic"""
    name: str = "RedScript Export"
    author: str = "RedScript Compiler"
    description: str = ""
    region_name: str = "Main"
    
@dataclass  
class ExportOptions:
    """Options for Litematica export"""
    include_support_blocks: bool = True  # Include stone under redstone
    include_air: bool = False            # Export air blocks
    offset: Tuple[int, int, int] = (0, 0, 0)  # Position offset

class LitematicaSerializer:
    """Serializes voxel grids to Minecraft Litematica format"""
    
    _block_state_mapping = None
    
    @classmethod
    def _get_block_state_mapping(cls):
        """Lazily initialize block state mapping (requires litemapy)"""
        if cls._block_state_mapping is None:
            if not LITEMAPY_AVAILABLE:
                raise ImportError("litemapy not installed. Install with: pip install litemapy")
            cls._block_state_mapping = {
                'minecraft:stone': BlockState('stone'),
                'minecraft:piston': BlockState('piston', facing='up'),
                'minecraft:sticky_piston': BlockState('sticky_piston', facing='up'),
                'minecraft:redstone_wire': BlockState('redstone_wire', power='15'),
                'minecraft:repeater': BlockState('repeater', facing='north', delay='1'),
                'minecraft:redstone_block': BlockState('redstone_block'),
                'minecraft:air': BlockState('air'),
            }
        return cls._block_state_mapping
    
    @staticmethod
    def serialize(voxel_grid: 'VoxelGrid', output_path: str) -> bool:
        """Serialize voxel grid to .litematic file"""
        if not LITEMAPY_AVAILABLE:
            raise ImportError("litemapy not installed. Install with: pip install litemapy")
        
        if not voxel_grid.blocks:
            return False
            
        # Calculate grid bounds
        xs = [x for x, _, _ in voxel_grid.blocks.keys()]
        ys = [y for _, y, _ in voxel_grid.blocks.keys()]
        zs = [z for _, _, z in voxel_grid.blocks.keys()]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        min_z, max_z = min(zs), max(zs)
        
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        length = max_z - min_z + 1
        
        # Create litemapy Region
        reg = Region(0, 0, 0, width, height, length)
        schem = reg.as_schematic(name="RedScript Export", author="RedScript", description="Exported from RedScript")
        
        for (x, y, z), block in voxel_grid.blocks.items():
            # Map to region coordinates
            rx = x - min_x
            ry = y - min_y
            rz = z - min_z
            
            # Get block state
            block_state = LitematicaSerializer.get_block_state(block.material, block.properties)
            
            # Set block
            reg.setblock(rx, ry, rz, block_state)
            
        # Save
        schem.save(output_path)
        return True
    
    @classmethod
    def get_block_state(cls, material: str, properties: Dict = None) -> Any:
        """Map material + properties to Minecraft BlockState"""
        if not LITEMAPY_AVAILABLE:
            return None
            
        name = material
        
        props = {}
        if properties:
            for k, v in properties.items():
                props[k] = str(v)
                
        return BlockState(name, **props)
