def get_neighbours_3x3(particle, GRID_ROWS, GRID_COLS, particles):
    OFFSETS2D = [
        (0, 0),
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
    ]

    cell_x, cell_y = particle.cell
    neighbours = []
    for offset in OFFSETS2D:
        new_x, new_y = cell_x + offset[0], cell_y + offset[1]
        if 0 <= new_x < GRID_ROWS and 0 <= new_y < GRID_COLS:
            neighbours.extend(particles[new_x][new_y])
    return neighbours
                
def update_cell(particle, GRID_ROWS, GRID_COLS, GRID_CELL_SIZE):
    particle_x, particle_y = particle.position.xy
    cell_x = int(particle_x // GRID_CELL_SIZE)
    cell_y = int(particle_y // GRID_CELL_SIZE)
    
    # Ensure cell coordinates are within the range of the grid
    cell_x = max(0, min(cell_x, GRID_ROWS - 1))
    cell_y = max(0, min(cell_y, GRID_COLS - 1))
    
    particle.cell = (cell_x, cell_y)

def create_particle_grid(GRID_ROWS, GRID_COLS):
    grid = []
    for x in range(GRID_ROWS + 1):
        a = []
        for y in range(GRID_COLS + 1):
            a.append([])
        grid.append(a)
    return grid