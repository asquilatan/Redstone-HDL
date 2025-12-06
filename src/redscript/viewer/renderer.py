"""
Voxel Renderer: Converts voxel grid to 3D entities
"""
from pathlib import Path
from typing import Dict, Tuple
from ursina import Entity, color, Vec3, Texture
from redscript.compiler.voxel_grid import VoxelGrid
from redscript.viewer.interactive import InteractiveBlockData

class VoxelRenderer:
    """Renders voxel blocks as 3D entities in Ursina"""
    
    # Rainbow-style colors for easy debugging
    BLOCK_COLORS = {
        'minecraft:stone': color.light_gray,
        'minecraft:piston': color.yellow,
        'minecraft:sticky_piston': color.orange,
        'minecraft:redstone_wire': color.red,
        'minecraft:repeater': color.lime,
        'minecraft:comparator': color.green,
        'minecraft:glass': color.azure,
        'minecraft:air': None,
        'minecraft:redstone_block': color.red,
        'minecraft:observer': color.violet,
        'minecraft:lever': color.brown,
        'minecraft:dropper': color.gray,
        'minecraft:hopper': color.dark_gray,
        'minecraft:target': color.pink,
        'minecraft:slime_block': color.lime,
        'minecraft:honey_block': color.gold,
        'minecraft:redstone_torch': color.orange,
        'minecraft:stone_pressure_plate': color.light_gray,
        'minecraft:stone_button': color.white,
        'minecraft:redstone_lamp': color.brown,
        'minecraft:lit_redstone_lamp': color.gold,
    }

    BLOCK_TEXTURES = {
        'minecraft:stone': 'stone.png',
        'minecraft:piston': 'piston.png',
        'minecraft:sticky_piston': 'sticky_piston.png',
        'minecraft:redstone_wire': 'redstone_wire.png',
        'minecraft:repeater': 'repeater.png',
        'minecraft:comparator': 'comparator.png',
        'minecraft:lever': 'lever.png',
        'minecraft:redstone_lamp': 'lamp_off.png',
        'minecraft:lit_redstone_lamp': 'lamp_on.png',
        'minecraft:stone_button': 'button.png',
        'minecraft:observer': 'observer.png',
        'minecraft:slime_block': 'slime.png',
        'minecraft:honey_block': 'honey.png',
        'minecraft:target': 'target.png',
        'minecraft:redstone_torch': 'redstone_torch.png',
    }

    @staticmethod
    def _get_redstone_connections(grid: VoxelGrid, x: int, y: int, z: int) -> Dict[str, bool]:
        """Check connections in N, S, E, W directions"""
        conns = {'n': False, 's': False, 'e': False, 'w': False}
        # North (-Z)
        if (x, y, z-1) in grid.blocks: conns['n'] = True
        # South (+Z)
        if (x, y, z+1) in grid.blocks: conns['s'] = True
        # East (+X)
        if (x+1, y, z) in grid.blocks: conns['e'] = True
        # West (-X)
        if (x-1, y, z) in grid.blocks: conns['w'] = True
        return conns

    @staticmethod
    def _get_wire_texture_and_rotation(conns: Dict[str, bool]) -> Tuple[str, int]:
        """Return texture name and rotation (degrees)"""
        n, s, e, w = conns['n'], conns['s'], conns['e'], conns['w']
        count = sum([n, s, e, w])
        
        if count == 0:
            return 'redstone_wire_dot.png', 0
        
        if count == 1:
            if n or s: return 'redstone_wire_line.png', 0
            if e or w: return 'redstone_wire_line.png', 90
            
        if count == 2:
            if n and s: return 'redstone_wire_line.png', 0
            if e and w: return 'redstone_wire_line.png', 90
            
            # Corners (Assuming Corner texture is Top-Left / N-W)
            if n and w: return 'redstone_wire_corner.png', 0
            if n and e: return 'redstone_wire_corner.png', 90
            if s and e: return 'redstone_wire_corner.png', 180
            if s and w: return 'redstone_wire_corner.png', 270
            
        if count == 3:
            # T-Shape (Assuming T texture points North / N-E-W)
            if not s: return 'redstone_wire_t.png', 0
            if not w: return 'redstone_wire_t.png', 90
            if not n: return 'redstone_wire_t.png', 180
            if not e: return 'redstone_wire_t.png', 270
            
        if count == 4:
            return 'redstone_wire_cross.png', 0
            
        return 'redstone_wire_dot.png', 0

    @staticmethod
    def render_grid(voxel_grid: VoxelGrid, parent_entity: Entity = None, simulator = None) -> list[Entity]:
        """Render the entire voxel grid"""
        from redscript.viewer.interactive import InteractiveBlock
        
        # Base path for textures (absolute path)
        base_tex_path = (Path(__file__).parent / 'textures').resolve()
        
        # Cache for loaded textures
        texture_cache = {}

        entities = []
        
        for (x, y, z), block in voxel_grid.blocks.items():
            if block.material == 'minecraft:air':
                continue
                
            col = VoxelRenderer.BLOCK_COLORS.get(block.material, color.magenta)
            tex_rel = VoxelRenderer.BLOCK_TEXTURES.get(block.material)
            
            tex_obj = None
            use_color = col
            rotation_y = 0
            
            if block.material == 'minecraft:redstone_wire':
                conns = VoxelRenderer._get_redstone_connections(voxel_grid, x, y, z)
                tex_rel, rotation_y = VoxelRenderer._get_wire_texture_and_rotation(conns)
            
            if block.material == 'minecraft:glass':
                use_color = color.rgba(0.5, 0.8, 1, 0.3) # Transparent light blue
            
            if tex_rel:
                # Try to load texture from file
                if tex_rel not in texture_cache:
                    full_path = base_tex_path / Path(tex_rel)
                    if full_path.exists():
                        try:
                            # Load texture using Ursina Texture class with absolute path
                            tex_obj = Texture(str(full_path))
                            texture_cache[tex_rel] = tex_obj
                            use_color = color.white
                        except Exception as e:
                            print(f"Warning: Failed to load texture {tex_rel}: {e}")
                            texture_cache[tex_rel] = None
                    else:
                        texture_cache[tex_rel] = None
                else:
                    tex_obj = texture_cache[tex_rel]
                    if tex_obj:
                        use_color = color.white
            
            if use_color is None and tex_obj is None:
                continue
            
            scale = Vec3(1, 1, 1)
            
            # Custom scaling for flat blocks
            if block.material == 'minecraft:redstone_wire':
                scale = Vec3(0.9, 0.1, 0.9)
            elif block.material in ['minecraft:repeater', 'minecraft:comparator']:
                scale = Vec3(0.9, 0.2, 0.9)
            elif block.material == 'minecraft:stone_pressure_plate':
                scale = Vec3(0.75, 0.1, 0.75)
            elif block.material == 'minecraft:stone_button':
                scale = Vec3(0.3, 0.2, 0.3)
            elif block.material == 'minecraft:redstone_torch':
                scale = Vec3(0.2, 0.5, 0.2)
            
            # Create interactive data
            block_data = InteractiveBlockData(
                block_id=f"{x}_{y}_{z}",
                material=block.material,
                properties=block.properties,
                position=(x, y, z),
                is_source=block.material in ['minecraft:lever', 'minecraft:stone_button'],
                is_toggleable=block.material in ['minecraft:repeater', 'minecraft:lever']
            )

            # Main block entity
            if simulator:
                e = InteractiveBlock(
                    simulator=simulator,
                    block_data=block_data,
                    model='cube',
                    color=use_color,
                    texture=tex_obj,
                    position=(x, y, z),
                    scale=scale,
                    rotation_y=rotation_y,
                    parent=parent_entity,
                    collider='box'
                )
            else:
                e = Entity(
                    model='cube',
                    color=use_color,
                    texture=tex_obj,
                    position=(x, y, z),
                    scale=scale,
                    rotation_y=rotation_y,
                    parent=parent_entity,
                    collider='box'
                )
                e.block_data = block_data
            
            # Handle transparency
            if block.material in ['minecraft:slime_block', 'minecraft:honey_block', 'minecraft:glass']:
                e.double_sided = True
                # If using color fallback, set alpha
                if not tex_obj:
                    e.alpha = 0.5
            
            # Add wireframe border (slightly larger)
            Entity(
                parent=e,
                model='wireframe_cube',
                color=color.black33,
                scale=1.02
            )
            
            entities.append(e)
            
        return entities
