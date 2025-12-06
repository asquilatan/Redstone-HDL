# Quickstart: Advanced Debugging & Components

## 1. Using Modules
Define reusable components with `module`.

```redscript
module DoublePistonExtender {
    p1 = StickyPiston(facing: up)
    p2 = StickyPiston(facing: up)
    
    p1.head -> p2.base
}

# Instantiate
dpe = DoublePistonExtender()
```

## 2. Debugging with Assertions
Verify your circuit behaves as expected.

```redscript
lever = Lever()
lamp = Lamp()

lever.signal -> lamp.power

# Assert lamp is off initially
assert(lamp.powered == false)

# Simulate interaction
lever.toggle()

# Assert lamp turns on
assert(lamp.powered == true)
```

## 3. Manual State Manipulation
Directly modify block state for testing.

```redscript
piston = Piston()

# Force piston to extend
piston.set_extended(true)

# Move a block manually
block = Stone(position: (0, 10, 0))
block.setPosition(0, 11, 0)
```

## 4. Debug Mode CLI
Run the compiler in debug mode to step through simulation.

```bash
redscript compile my_circuit.rs --debug
```

Output:
```text
Tick 0:
  lever: off
  lamp: off
> step
Tick 1:
  lever: on (toggled)
  lamp: off (delay)
> step
Tick 2:
  lever: on
  lamp: on
```
