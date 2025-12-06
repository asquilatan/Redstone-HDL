"""
RedScript package initialization
"""
__version__ = '0.1.0a1'
__author__ = 'Redstone HDL Contributors'

from .compiler.compiler import Compiler
from .compiler.voxel_grid import VoxelGrid, Block
from .compiler.logical_graph import LogicalGraph, Component

__all__ = [
    'Compiler',
    'VoxelGrid',
    'Block',
    'LogicalGraph',
    'Component',
]
