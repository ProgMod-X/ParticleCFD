import particle
import math


class Grid:
    def __init__(self, screen_width: int, screen_height: int, cell_size: int) -> None:
        self.width = screen_width
        self.height = screen_height
        self.size = cell_size
        self.cells = {}

    def add_particle(self, particle: particle.Particle) -> None:
        col_idx = math.floor(particle.position.x / self.size)
        row_idx = math.floor(particle.position.y / self.size)

        cell = self.cells.get((col_idx, row_idx), [])
        cell.append(particle)
        self.cells[(col_idx, row_idx)] = cell
        particle.grid_cell = (col_idx, row_idx)

    def remove_particle(self, particle: particle.Particle) -> None:
        col_idx, row_idx = particle.grid_cell
        cell = self.cells.get((col_idx, row_idx), [])
        cell.remove(particle)
        if not cell:
            del self.cells[(col_idx, row_idx)]

    def get_neighbours(self, particle: particle.Particle) -> list[particle.Particle]:
        idx = particle.grid_cell
        neighbours = []

        for i in range(idx[0] - 1, idx[0] + 2):
            for j in range(idx[1] - 1, idx[1] + 2):
                cell = self.cells.get((i, j), [])
                for p in cell:
                    if p != particle:
                        neighbours.append(p)

        return neighbours

    def get_all_particles(self) -> list[particle.Particle]:
        all_particles = []
        for cell in self.cells.values():
            all_particles.extend(cell)
        return all_particles
