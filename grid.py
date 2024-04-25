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

        self.cells[col_idx][row_idx].append(particle)
        particle.grid_cell = (col_idx, row_idx)

    def remove_particle(self, particle: particle.Particle) -> None:
        col_idx, row_idx = particle.grid_cell
        cell = self.cells[col_idx][row_idx]
        # p_idx = cell.index(particle)
        cell.remove(particle)

    def get_neighbours(self, particle: particle.Particle) -> list[particle.Particle]:
        top_left = [
            math.floor((particle.position.x - particle.size) / self.size),
            math.floor((particle.position.y - particle.size) / self.size),
        ]

        bottom_right = [
            math.floor((particle.position.x + particle.size) / self.size),
            math.floor((particle.position.y + particle.size) / self.size),
        ]

        neighbours = []
        for i in range(top_left[0], bottom_right[0] + 1):
            for j in range(top_left[1], bottom_right[1] + 1):
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