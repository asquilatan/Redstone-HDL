"""
Camera Controls: Spectator mode
"""
from ursina import Entity, Vec3, camera, held_keys, time, mouse, clamp, raycast
import math

class SpectatorController(Entity):
    """
    Spectator camera controller.
    WASD: Move horizontal
    Space/Shift: Move vertical
    Mouse: Look
    Scroll: Adjust speed
    """
    
    def __init__(self, **kwargs):
        super().__init__()
        self.speed = 10
        self.mouse_sensitivity = Vec3(40, 40, 0)
        self.enabled = True
        self.mouse_locked = True
        
        # UI Elements
        self.pos_text = kwargs.get('pos_text')
        self.look_text = kwargs.get('look_text')
        
        # Initial camera setup
        camera.parent = self
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 90  # Wider FOV
        
        # Input state
        mouse.locked = True
        mouse.visible = False
        
    def update(self):
        if not self.enabled:
            return

        # Only rotate if mouse is locked
        if self.mouse_locked:
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity.x
            self.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity.y
            self.rotation_x = clamp(self.rotation_x, -90, 90)
        
        # Movement (always available)
        direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            + self.up * (held_keys['space'] - held_keys['shift'])
        ).normalized()
        
        self.position += direction * self.speed * time.dt
        
        # Update UI
        if self.pos_text:
            # We want world coordinates, but maybe relative to grid?
            # For now, just show camera world position
            self.pos_text.text = f"Pos: ({self.position.x:.1f}, {self.position.y:.1f}, {self.position.z:.1f})"
            
        if self.look_text:
            hit = raycast(self.position, self.forward, distance=100, ignore=[self])
            if hit.hit and hit.entity:
                # Check for block_data
                if hasattr(hit.entity, 'block_data'):
                    bd = hit.entity.block_data
                    props = ", ".join([f"{k}={v}" for k, v in bd.properties.items()])
                    self.look_text.text = f"Looking at: {bd.material} {bd.position}\nProps: {props}"
                else:
                    # hit.entity.position is local to grid_parent, so it matches grid coordinates
                    pos = hit.entity.position
                    self.look_text.text = f"Looking at: ({int(pos.x)}, {int(pos.y)}, {int(pos.z)})"
            else:
                self.look_text.text = "Looking at: None"
        
    def input(self, key):
        if key == 'scroll up':
            self.speed += 2
        if key == 'scroll down':
            self.speed = max(1, self.speed - 2)
        if key == 'escape':
            self.mouse_locked = not self.mouse_locked
            mouse.locked = self.mouse_locked
            mouse.visible = not self.mouse_locked
            
    def setup_for_grid(self, center: tuple[float, float, float]):
        """Position camera to view the grid center"""
        # Position camera offset from center
        offset = Vec3(-15, 12, -15)
        self.position = Vec3(*center) + offset
        
        # Calculate rotation to look at center (without using look_at which can cause roll)
        direction = Vec3(*center) - self.position
        
        # Calculate yaw (rotation around Y axis)
        yaw = math.degrees(math.atan2(direction.x, direction.z))
        
        # Calculate pitch (rotation around X axis)
        horizontal_dist = math.sqrt(direction.x**2 + direction.z**2)
        pitch = -math.degrees(math.atan2(direction.y, horizontal_dist))
        
        self.rotation = (pitch, yaw, 0)  # No roll
