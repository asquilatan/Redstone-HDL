from PIL import Image, ImageDraw
import os
from pathlib import Path

# Define colors
RED = (255, 0, 0, 255)
DARK_RED = (180, 0, 0, 255)
TRANSPARENT = (0, 0, 0, 0)

# Output directory
output_dir = Path(r'd:\Program Files\VS Code Programs\Redstone_HDL\src\redscript\viewer\textures')
output_dir.mkdir(parents=True, exist_ok=True)

def create_texture(name, draw_func):
    img = Image.new('RGBA', (16, 16), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    draw_func(draw)
    img.save(output_dir / name)
    print(f"Created {name}")

def draw_dot(draw):
    # Central dot (4x4)
    draw.rectangle([6, 6, 9, 9], fill=RED)
    draw.rectangle([7, 7, 8, 8], fill=DARK_RED)

def draw_line(draw):
    # Vertical line
    draw.rectangle([6, 0, 9, 15], fill=RED)
    draw.rectangle([7, 0, 8, 15], fill=DARK_RED)

def draw_corner(draw):
    # Bottom-Right corner (South-East)
    # Vertical part (South)
    draw.rectangle([6, 8, 9, 15], fill=RED)
    draw.rectangle([7, 8, 8, 15], fill=DARK_RED)
    # Horizontal part (East)
    draw.rectangle([8, 6, 15, 9], fill=RED)
    draw.rectangle([8, 7, 15, 8], fill=DARK_RED)
    # Center connection
    draw.rectangle([6, 6, 9, 9], fill=RED)

def draw_t(draw):
    # T-junction (North, East, West)
    # Vertical part (North)
    draw.rectangle([6, 0, 9, 8], fill=RED)
    draw.rectangle([7, 0, 8, 8], fill=DARK_RED)
    # Horizontal part (East-West)
    draw.rectangle([0, 6, 15, 9], fill=RED)
    draw.rectangle([0, 7, 15, 8], fill=DARK_RED)
    # Center connection
    draw.rectangle([6, 6, 9, 9], fill=RED)

def draw_cross(draw):
    # Cross (All directions)
    # Vertical part
    draw.rectangle([6, 0, 9, 15], fill=RED)
    draw.rectangle([7, 0, 8, 15], fill=DARK_RED)
    # Horizontal part
    draw.rectangle([0, 6, 15, 9], fill=RED)
    draw.rectangle([0, 7, 15, 8], fill=DARK_RED)
    # Center connection
    draw.rectangle([6, 6, 9, 9], fill=RED)

if __name__ == "__main__":
    create_texture('redstone_wire_dot.png', draw_dot)
    create_texture('redstone_wire_line.png', draw_line)
    create_texture('redstone_wire_corner.png', draw_corner)
    create_texture('redstone_wire_t.png', draw_t)
    create_texture('redstone_wire_cross.png', draw_cross)
