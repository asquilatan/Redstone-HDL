module DoublePistonExtender(x, y, z, facing) {
    # A standard vertical double piston extender structure
    
    # Bottom Piston
    def bottom sticky_piston(
        pos=(x, y, z), 
        facing=facing
    )
    
    # Top Piston
    def top sticky_piston(
        pos=(x, y + 1, z), 
        facing=facing
    )
    
    # The block being moved (initially on top)
    def payload stone(
        pos=(x, y + 2, z)
    )
    
    # Placeholder for control circuit inputs
    # In a full HDL, we might define ports here
    # connection port_ref -> port_ref
}

module TriplePistonExtender(x, y, z) {
    def p1 sticky_piston(pos=(x, y, z), facing="up")
    def p2 sticky_piston(pos=(x, y+1, z), facing="up")
    def p3 sticky_piston(pos=(x, y+2, z), facing="up")
    def payload stone(pos=(x, y+3, z))
}
