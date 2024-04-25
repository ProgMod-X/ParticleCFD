import particle
import math


class Grid:
    def __init__(self, screen_width: int, screen_height: int, cell_size: int) -> list:
        self.width = screen_width
        self.height = screen_height
        self.size = cell_size
        self.num_of_cols = math.ceil(self.width / self.size)
        self.num_of_rows = math.ceil(self.height / self.size)
        self.cells = []

        for i in range(self.num_of_cols):
            self.cells.append([])
            for j in range(self.num_of_rows):
                self.cells[i].append([])

    def add_particle(self, particle: particle.Particle) -> None:
        col_idx = math.floor(particle.position.x / self.size)
        row_idx = math.floor(particle.position.y / self.size)

        # Clamp column index to stay within range [0, num_of_cols - 1]
        col_idx = max(0, min(col_idx, self.num_of_cols - 1))
        # Clamp row index to stay within range [0, num_of_rows - 1]
        row_idx = max(0, min(row_idx, self.num_of_rows - 1))

        self.cells[col_idx][row_idx].append(particle)
        particle.grid_cell = (col_idx, row_idx)

    def remove_particle(self, particle: particle.Particle) -> None:
        col_idx, row_idx = particle.grid_cell
        cell = self.cells[col_idx][row_idx]
        # p_idx = cell.index(particle)
        cell.remove(particle)

    def get_neighbours(self, particle: particle.Particle) -> list[particle.Particle]:
        idx = particle.grid_cell

        neighbours = []
        for i in range(idx[0] - 1, idx[0] + 2):
            for j in range(idx[1], idx[1] + 2):
                if i < 0 or j < 0 or i >= self.num_of_cols or j >= self.num_of_rows:
                    continue
                c = self.cells[i][j]
                for p in c:
                    if p != particle:
                        neighbours.append(p)

        return neighbours

    def get_all_particles(self) -> list[particle.Particle]:
        all_particles = []
        for col in self.cells:
            for row in col:
                all_particles.extend(row)
        return all_particles