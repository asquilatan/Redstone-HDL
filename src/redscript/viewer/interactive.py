from dataclasses import dataclass
from typing import Dict, Tuple
from ursina import Entity, color, mouse

@dataclass
class InteractiveBlockData:
    """Metadata attached to rendered entities for interaction"""
    block_id: str                    # Unique ID in voxel grid
    material: str                    # e.g., "minecraft:repeater"
    properties: Dict[str, str]       # e.g., {"delay": "2", "facing": "north"}
    position: Tuple[int, int, int]   # Grid coordinates
    is_source: bool = False          # Can emit signals (lever, button)
    is_toggleable: bool = False      # Can be clicked to change state

class InteractiveBlock(Entity):
    def __init__(self, simulator, block_data: InteractiveBlockData, **kwargs):
        super().__init__(**kwargs)
        self.simulator = simulator
        self.block_data = block_data
        
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                self.on_click()
            elif key == 'right mouse down':
                self.on_right_click()
                
    def on_click(self):
        if self.block_data.is_source or self.block_data.is_toggleable:
            self.simulator.toggle_source(self.block_data.block_id)
            self.update_visuals()
            
    def on_right_click(self):
        if self.block_data.material == 'minecraft:repeater':
            delay = int(self.block_data.properties.get('delay', 1))
            delay = (delay % 4) + 1
            self.block_data.properties['delay'] = str(delay)
            
    def update_visuals(self):
        state = self.simulator.get_power_state(self.block_data.block_id)
        if state:
            if state.is_powered:
                if self.block_data.material == 'minecraft:redstone_lamp':
                    # We need to access renderer textures, but for now just use color tint or something
                    self.color = color.white
                elif self.block_data.material == 'minecraft:lever':
                    self.color = color.white
            else:
                if self.block_data.material == 'minecraft:redstone_lamp':
                    self.color = color.gray
