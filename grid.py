import particle
import numpy as np
# import line_profiler

class Grid:
    def __init__(self, screen_width: int, screen_height: int, cell_size: int) -> None:
        self.width = screen_width
        self.height = screen_height
        self.size = cell_size
        self.cells = np.empty((int(np.ceil(screen_width / cell_size)), int(np.ceil(screen_height / cell_size))), dtype=object)

    # @line_profiler.profile
    def add_particle(self, particle: particle.Particle) -> None:
        col_idx = int(np.floor(particle.position.x / self.size))
        row_idx = int(np.floor(particle.position.y / self.size))

        if self.cells[col_idx, row_idx] is None:
            self.cells[col_idx, row_idx] = [particle]
        else:
            self.cells[col_idx, row_idx].append(particle)

        particle.grid_cell = (col_idx, row_idx)

    # @line_profiler.profile
    def remove_particle(self, particle: particle.Particle) -> None:
        col_idx, row_idx = particle.grid_cell
        cell = self.cells[col_idx, row_idx]

        if cell:  # Check if cell is not empty
            cell.remove(particle)
            if not cell:
                self.cells[col_idx, row_idx] = None

    # @line_profiler.profile
    def get_neighbours(self, particle: particle.Particle) -> list[particle.Particle]:
        col_idx, row_idx = particle.grid_cell
        neighbours = []
        search_range = 1  # Look for neighbors within a 1-cell radius

        grid_bound_x, grid_bound_y = self.cells.shape

        for i in range(max(0, col_idx - search_range), min(col_idx + search_range + 1, grid_bound_x)):
            for j in range(max(0, row_idx - search_range), min(row_idx + search_range + 1, grid_bound_y)):
                cell = self.cells[i, j]
                if cell is not None:
                    neighbours.extend(cell)
        if particle in neighbours:
            neighbours.remove(particle)  # Exclude the particle itself
        return neighbours

    # @line_profiler.profile
    def get_all_particles(self) -> list[particle.Particle]:
        all_particles = []
        for cell in self.cells.flat:
            if cell is not None:
                all_particles.extend(cell)
        return all_particles
