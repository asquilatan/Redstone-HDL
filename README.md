# RedScript

RedScript (formerly RedScript HDL) is a Hardware Description Language (HDL) for Minecraft Redstone. It allows you to define circuits using high-level code and compile them into Litematica schematics.

## Features

- **High-Level Syntax**: Define components and connections easily.
- **Compilation**: Generates `.litematic` files for use with Litematica mod.
- **Simulation**: (Experimental) Simulate circuit logic.
- **3D Viewer**: Preview your circuit before building.

## Supported Components

- **Basic**: Redstone Wire, Torch, Block, Lever
- **Logic**: Repeater, Comparator
- **Mechanics**: Piston, Sticky Piston, Slime Block, Honey Block
- **Input/Output**: Button, Pressure Plate, Lamp, Target Block, Note Block, Dropper, Hopper, Observer

## Usage

1. Write your script (e.g., `circuit.rs`):
   ```rust
   def button Button(pos=(0, 5, 0))
   def lamp Lamp(pos=(2, 5, 0))
   button.signal -> lamp.power
   ```

2. Compile and View:
   ```bash
   redscript compile circuit.rs --view
   ```

## Syntax Guide

### 1. Defining Components
Components are the building blocks of your circuit. You define them using the `def` keyword.

```rust
// Define a stone block at (0, 0, 0)
def s1 Stone(pos=(0, 0, 0))

// Define a piston facing up
def p1 Piston(pos=(0, 1, 0), facing="up")

// Define a sticky piston facing north
def sp StickyPiston(pos=(0, 2, 0), facing="north")

// Define a repeater with 2 ticks delay
def r1 Repeater(pos=(1, 0, 0), delay=2, facing="east")
```

### 2. Modules
Modules allow you to create reusable sub-circuits. They act like functions that can instantiate multiple components.

#### Defining a Module
Create a module in a purely definition file (e.g., `lib.rs`) or at the top of your script.

```rust
// A simple module that places a piston and a block on top
module PistonPusher(x, y, z) {
    def p Piston(pos=(x, y, z), facing="up")
    def b Stone(pos=(x, y+1, z))
}
```

#### Using a Module
Instantiate a module just like a component.

```rust
// Create one pusher
def pusher1 PistonPusher(x=10, y=5, z=10)
```

### 3. Imports
Split your code into multiple files for better organization.

#### Basic Import
Import all modules from another file.

```rust
import "modules/my_lib.rs"

def m MyModule(x=0)
```

#### Selective Import
Import only specific modules.

```rust
from "modules/mechanisms.rs" import PistonDoor, Extender

def door PistonDoor(x=0, y=4, z=0)
```

### 4. Control Flow
Use loops and conditionals to procedurally generate circuits.

#### Loops
Great for creating arrays of components.

```rust
// Create a row of 10 lamps
for i in range(0, 10) {
    def lamp Lamp(pos=(i, 0, 0))
}
```

#### Conditionals
Conditional logic based on parameters.

```rust
module SmartColumn(height, has_light) {
    for y in range(0, height) {
        def block Stone(pos=(0, y, 0))
        
        if (has_light == 1) {
            def l Lamp(pos=(1, y, 0))
        }
    }
}
```

## Debugging

RedScript includes a powerful debug mode for stepping through your circuit's logic.

```bash
redscript compile circuit.rs --debug
```

- **Step-by-Step**: Execute one tick at a time.
- **Inspect**: View component states and signal strengths.
- **Assert**: Verify circuit behavior with `assert(condition)`.

## Interactive Viewer

The 3D viewer now supports:
- **Textures**: Blocks are rendered with 16x16 textures.
- **Interaction**: Click buttons/levers to toggle, right-click repeaters to cycle delay.
- **Block Info**: Hover over blocks to see details.
- **Export**: Press F10 to export to `.litematic`.

## Export

You can export your design to a Litematica schematic:

```bash
redscript export my_design.rs --output my_design.litematic
```

## Why did I make this?

I wanted to see AI create decently complex redstone contraptions in Minecraft. However, going through the YouTube dumpster fire that is "I Asked AI To Make Redstone For Me" slop, I realized that clankers like ChatGPT and Gemini weren't being given a structured, machine-readable language for describing redstone logic. I was appalled, not by the work of the AI (because it's obviously garbage, duh), but by incompetence of the creators for not providing that essential tool in the first place. So I made RedScript, which acts as an intermediate step between AI and Minecraft Schematics. 

In hindsight, I probably could've just read the .litematic files but whatever.