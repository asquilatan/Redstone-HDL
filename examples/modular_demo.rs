# Demonstrate modularity by importing mechanical components
from "examples/modules/piston_mechanisms.rs" import DoublePistonExtender, TriplePistonExtender

# Create a row of Double Piston Extenders
module ExtenderArray(count, start_x, y, z) {
    for i in range(0, count) {
        def dpe DoublePistonExtender(
            x = start_x + (i * 2), # Space them out
            y = y,
            z = z,
            facing = "up"
        )
    }
}

# Instantiate the array
def array1 ExtenderArray(count=5, start_x=0, y=3, z=0)

# Manually instantiate one at a different location
def dpe_solo DoublePistonExtender(x=0, y=1, z=5, facing="up")

def tpe_solo TriplePistonExtender(x=0, y=1, z=7)

