module PistonColumn(height, x_pos) {
    for i in range(0, height) {
        def p piston(
            pos=(x_pos, i, 0),
            facing="up"
        )
        
        if (i > 2) {
            def g glass(pos=(x_pos + 1, i, 0))
        } else {
            def s stone(pos=(x_pos + 1, i, 0))
        }
    }
}

def col1 PistonColumn(height=5, x_pos=0)
