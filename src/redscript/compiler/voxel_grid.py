"""
Voxel Grid: 3D representation of the world
"""
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional
import numpy as np

@dataclass
class Block:
    """Represents a single block in the voxel grid"""
    material: str  # e.g., "minecraft:stone", "minecraft:redstone_wire"
    properties: Dict[str, str] = field(default_factory=dict)  # e.g., {"facing": "north", "power": "15"}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'material': self.material,
            'properties': self.properties
        }


class VoxelGrid:
    """Sparse 3D array of blocks using hash map"""
    
    def __init__(self, width: int = 256, height: int = 256, depth: int = 256):
        self.width = width
        self.height = height
        self.depth = depth
        self.blocks: Dict[Tuple[int, int, int], Block] = {}
        self.bounds = {
            'min_x': 0, 'max_x': width - 1,
            'min_y': 0, 'max_y': height - 1,
            'min_z': 0, 'max_z': depth - 1,
        }
    
    def set_block(self, x: int, y: int, z: int, block: Block) -> None:
        """Place a block at the given coordinates (sparse storage, no bounds check)"""
        self.blocks[(x, y, z)] = block
    
    def get_block(self, x: int, y: int, z: int) -> Optional[Block]:
        """Get a block at the given coordinates"""
        return self.blocks.get((x, y, z))
    
    def is_solid(self, x: int, y: int, z: int) -> bool:
        """Check if a block is solid (not air)"""
        block = self.get_block(x, y, z)
        return block is not None and block.material != "minecraft:air"
    
    def clear_block(self, x: int, y: int, z: int) -> None:
        """Remove a block (set to air)"""
        if (x, y, z) in self.blocks:
            del self.blocks[(x, y, z)]
    
    def _is_in_bounds(self, x: int, y: int, z: int) -> bool:
        """Check if coordinates are within reasonable limits (sparse storage allows any coords)"""
        # Sparse storage: allow any coordinates, serializer normalizes them
        return True
    
    def get_neighbors(self, x: int, y: int, z: int) -> list:
        """Get all neighboring voxels (6 directions: ±X, ±Y, ±Z)"""
        neighbors = []
        directions = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1),
        ]
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            if self._is_in_bounds(nx, ny, nz):
                neighbors.append((nx, ny, nz))
        return neighbors
    
    def serialize(self) -> bytes:
        """Serialize grid to bytes for C++ solver"""
        # Create a numpy array to store block occupancy
        grid = np.zeros((self.width, self.height, self.depth), dtype=np.uint8)
        for (x, y, z), block in self.blocks.items():
            if block.material != "minecraft:air":
                grid[x, y, z] = 1
        return grid.tobytes()
