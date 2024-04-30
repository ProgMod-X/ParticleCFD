import particle
import numpy as np
import line_profiler

class Grid:
    def __init__(self, screen_width: int, screen_height: int, cell_size: int) -> None:
        self.width = screen_width
        self.height = screen_height
        self.size = cell_size
        self.cells = {}  # Use a dictionary for efficient neighbor lookup

    def add_particle(self, particle: particle.Particle) -> None:
        col_idx = int(np.floor(particle.position.x / self.size))
        row_idx = int(np.floor(particle.position.y / self.size))

        cell = self.cells.get((col_idx, row_idx), [])  # Get or create cell list
        cell.append(particle)
        self.cells[(col_idx, row_idx)] = cell
        particle.grid_cell = (col_idx, row_idx)

    def remove_particle(self, particle: particle.Particle) -> None:
        col_idx, row_idx = particle.grid_cell
        cell = self.cells.get((col_idx, row_idx), [])

        if cell:  # Check if cell exists before removal
            cell.remove(particle)
            if not cell:
                del self.cells[(col_idx, row_idx)]

    # @line_profiler.profile
    def get_neighbours(self, particle: particle.Particle) -> list[particle.Particle]:
        col_idx, row_idx = particle.grid_cell
        neighbours = []
        search_range = 1  # Look for neighbors within a 1-cell radius

        grid_bound_x = self.width // self.size
        grid_bound_y = self.height // self.size

        for i in range(col_idx - search_range, col_idx + search_range + 1):
            for j in range(row_idx - search_range, row_idx + search_range + 1):
                # Ensure valid cell indices within grid bounds
                if 0 <= i < grid_bound_x and 0 <= j < grid_bound_y:
                    cell = self.cells.get((i, j), [])
                    neighbours.extend(cell)
        if particle in neighbours:
            neighbours.remove(particle)  # Exclude the particle itself
        return neighbours

    def get_all_particles(self) -> list[particle.Particle]:
        all_particles = []
        for cell in self.cells.values():
            all_particles.extend(cell)
        return all_particles
