# RedScript Modular Examples
# Demonstrating: T-FlipFlop, Observer Clock, Torch Tower, Slime Piston Tower, 2x2 Door
# Using the new 'module' syntax.

# ------------------------------------------------------------------
# Module 1: T-FlipFlop (Compact Design)
# Coordinates: Offset (0, 0, 0)
# ------------------------------------------------------------------
module TFlipFlop() {
    # Input Trigger (Button)
    # Support block under manual button placement
    btn_sup = Stone(position: (0, 1, -1))
    btn = Button(position: (0, 2, -1), facing: south)
    
    # Pulse Generator (Observer)
    obs = Observer(position: (0, 2, 0), facing: south)
    
    # Mechanism (Sticky Piston + Block)
    piston = StickyPiston(position: (0, 1, 1), facing: up)
    rs_block = Block(material: "minecraft:redstone_block", position: (0, 2, 1))
    
    # Output Indicator (Lamp)
    lamp = Lamp(position: (0, 3, 2))
    
    assert(piston.facing == up)
}

# ------------------------------------------------------------------
# Module 2: Observer Clock
# Coordinates: Offset (10, 0, 0)
# ------------------------------------------------------------------
module ObserverClock() {
    # Observer 1 facing South
    obs1 = Observer(position: (10, 2, 0), facing: south)
    # Observer 2 facing North
    obs2 = Observer(position: (10, 2, 1), facing: north)
    
    # Output Tap
    # Wire needs support
    sup_tap = Stone(position: (10, 2, 0)) # Occupied by Obs1?
    # Obs1 is at (10, 2, 0).
    # Wire at (10, 3, 0) is on TOP of Obs1.
    # Obs1 is solid? Observers are solid blocks.
    # So Wire on top of Obs1 is VALID support.
    
    wire_tap = RedstoneWire(position: (10, 3, 0), power: 15)
}

# ------------------------------------------------------------------
# Module 3: Redstone Torch Tower
# Coordinates: Offset (20, 0, 0)
# ------------------------------------------------------------------
module TorchTower() {
    # Base Input
    base_sup = Stone(position: (20, 0, -1)) # Support for lever
    lever = Lever(position: (20, 1, -1), facing: south)
    
    base = Stone(position: (20, 1, 0))
    # Lever connects to Base? Physically adjacent.
    
    # Inverter 1
    torch1 = RedstoneTorch(position: (20, 2, 0))
    block1 = Stone(position: (20, 3, 0))
    
    # Inverter 2
    torch2 = RedstoneTorch(position: (20, 4, 0))
    block2 = Stone(position: (20, 5, 0))
    
    # Output Lamp
    lamp = Lamp(position: (20, 6, 0))
}

# ------------------------------------------------------------------
# Module 4: Slime Piston Tower (Vertical Signal)
# Coordinates: Offset (30, 0, 0)
# ------------------------------------------------------------------
module SlimePistonTower() {
    # Input
    in_sup = Stone(position: (30, 0, -1))
    btn = Button(position: (30, 1, -1), facing: south)
    
    in_block = Stone(position: (30, 1, 0))
    
    # Wire Logic
    # Wire(30, 2, -1) needs support at (30, 1, -1)
    # (30, 1, -1) is occupied by 'btn'.
    # Can't check "block below" if block below is non-solid Button.
    # But Button IS non-solid.
    # So Wire cannot be on top of Button.
    # We need a block above the button?
    # Or Wire on side?
    # Wire at (30, 2, -1). Below is (30, 1, -1).
    # (30, 1, -1) is the Button.
    # So Wire is floating on Button.
    # Fix: Move Wire or move Button.
    # Button on face of block (30, 1, 0).
    # Wire on top of block (30, 2, 0)?
    # Piston is at (30, 2, 0).
    # So Wire must be adjacent.
    # Wire at (30, 2, -1). Support at (30, 1, -1).
    # Fix: Support Block at (30, 1, -1).
    # Button at (30, 1, -2). Support at (30, 0, -2).
    
    btn_sup2 = Stone(position: (30, 0, -2))
    btn2 = Button(position: (30, 1, -2), facing: south)
    wire_sup = Stone(position: (30, 1, -1))
    wire1 = RedstoneWire(position: (30, 2, -1), power: 15)
    
    # Piston 1
    pist1 = StickyPiston(position: (30, 2, 0), facing: up)
    
    # Payload 1
    slime1 = SlimeBlock(position: (30, 3, 0))
    
    # Detector 1
    obs1 = Observer(position: (31, 3, 0), facing: west)
    
    # Signal Transmission
    # Obs1(31,3,0) -> Link Block(32,3,0)
    link_block = Stone(position: (32, 3, 0))
    
    # Wire Sequence up
    # Wire(32, 4, 0) needs support(32, 3, 0) [OK - link_block]
    link_wire1 = RedstoneWire(position: (32, 4, 0), power: 15)
    
    # Wire(31, 5, 0) needs support(31, 4, 0)
    # (31, 4, 0) is Air. Needs Stone.
    sup_link2 = Stone(position: (31, 4, 0))
    link_wire2 = RedstoneWire(position: (31, 5, 0), power: 15)
    
    # Piston 2
    pist2 = StickyPiston(position: (30, 5, 0), facing: up)
    slime2 = SlimeBlock(position: (30, 6, 0))
    
    # Detector 2
    obs2 = Observer(position: (31, 6, 0), facing: west)
    out_lamp = Lamp(position: (32, 6, 0))
}

# ------------------------------------------------------------------
# Module 5: Simple 2x2 Piston Door
# Coordinates: Offset (40, 0, 0)
# ------------------------------------------------------------------
module Door2x2() {
    # Door Blocks
    d00 = Stone(position: (40, 2, 5))
    d10 = Stone(position: (41, 2, 5))
    d01 = Stone(position: (40, 3, 5))
    d11 = Stone(position: (41, 3, 5))
    
    # Pistons
    lp0 = StickyPiston(position: (38, 2, 5), facing: east)
    lp1 = StickyPiston(position: (38, 3, 5), facing: east)
    rp0 = StickyPiston(position: (43, 2, 5), facing: west)
    rp1 = StickyPiston(position: (43, 3, 5), facing: west)
    
    # Wiring Roof
    roof_l = Stone(position: (38, 5, 5))
    roof_r = Stone(position: (43, 5, 5))
    roof_bridge = Stone(position: (39, 5, 5))
    roof_mid = Stone(position: (40, 5, 5)) 
    roof_mid2 = Stone(position: (41, 5, 5))
    roof_bridge2 = Stone(position: (42, 5, 5))
    
    # Lever Input
    sup_lev = Stone(position: (45, 1, 5))
    lever = Lever(position: (45, 2, 5), facing: west)
    
    assert(lp0.type == StickyPiston)
}

# ------------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------------

tff = TFlipFlop()
clk = ObserverClock()
tow = TorchTower()
spt = SlimePistonTower()
dor = Door2x2()
