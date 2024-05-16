import pygame
import numpy as np
import particle
import time
import random
import math

import line_profiler
# kernprof -l .\main.py
# python.exe -m line_profiler .\main.py.lprof

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 1000
NUM_OF_PARTICLES = 1000
DAMPENING_EFFECT = 0.75
NEAR_DISTANCE_REQUIRED = 20  # Pixels
PARTICLE_PIXEL_RADIUS = 3.5
REPULSION_COEFF = 1E3
REPULSION_DROPOFF = 6E-2
GRAVITY = pygame.Vector2(0, 9.81 * 1e4)

GRID_CELL_SIZE = NEAR_DISTANCE_REQUIRED
GRID_ROWS = math.ceil(HEIGHT / GRID_CELL_SIZE)
GRID_COLS = math.ceil(WIDTH / GRID_CELL_SIZE)

# Colors
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("PCFD")

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

forces = {}

def create_particle_grid():
    grid = []
    for x in range(GRID_ROWS):
        a = []
        for y in range(GRID_COLS):
            a.append([])
        grid.append(a)
    return grid

new_particles = create_particle_grid()

def deltaTime() -> float:
    # Get the current time in seconds
    current_time = time.time()

    # Calculate the difference between the current time and the last time deltaTime was called
    if "last_time" not in deltaTime.__dict__:
        deltaTime.last_time = current_time
    delta_time = current_time - deltaTime.last_time

    # Update the last_time for the next deltaTime call
    deltaTime.last_time = current_time

    return delta_time



def force(iter_particle: particle.Particle, particle: particle.Particle) -> pygame.Vector2:
    f = pygame.Vector2(0)
    
    diff = iter_particle.position - particle.position

    distance = diff.length()

    if distance == 0:
        return pygame.Vector2(0)

    direction = diff.normalize()
    
    f += repulsion(distance, direction)
    f += viscosity(iter_particle, particle, distance)

    return f



def repulsion(distance, direction) -> pygame.Vector2:
    repulsion_force = pygame.Vector2(0)

    force_magnitude = REPULSION_COEFF / ((distance) * REPULSION_DROPOFF) ** 2

    repulsion_force -= direction * force_magnitude

    return repulsion_force



def viscosity(
    iter_particle: particle.Particle, particle: particle.Particle, distance
) -> pygame.Vector2:
    viscosity_force = pygame.Vector2(0)

    viscosity_force = (iter_particle.velocity - particle.velocity) * (
        3 / (distance / PARTICLE_PIXEL_RADIUS)**2
    )

    return viscosity_force

def get_neighbours_3x3(particle):
    cell_x, cell_y = particle.cell
    neighbours = []
    for offset in OFFSETS2D:
        try:
            neighbours.extend(new_particles[cell_x + offset[0]][cell_y + offset[1]])
        except:
            continue
    return neighbours
                
def update_cell(particle):
    particle_x, particle_y = particle.position.xy
    cell_x = int(particle_x // GRID_CELL_SIZE)
    cell_y = int(particle_y // GRID_CELL_SIZE)
    particle.cell = (cell_x, cell_y)
                
def simulate(dt):
    WIN.fill((0, 0, 0))

    for x in range(GRID_ROWS):
        for y in range(GRID_COLS):
            for particle in new_particles[x][y]:
                
                update_cell(particle)   
    
    for x in range(GRID_ROWS):
        for y in range(GRID_COLS):
            for particle in new_particles[x][y]:
                neighbours = get_neighbours_3x3(particle)
                f = pygame.Vector2(0)
                for iter_particle in neighbours:
                    f += force(iter_particle, particle)
                forces[particle] = f

                particle.velocity += forces[particle] * dt
                particle.position += particle.velocity * dt



def render():
    for x in range(GRID_ROWS):
        for y in range(GRID_COLS):
            for p in new_particles[x][y]:
                p.draw(WIN)

    pygame.display.flip()



def setup():
    global GRID_ROWS, GRID_COLS, new_particles
    width, height = pygame.display.get_window_size()

    GRID_ROWS = math.ceil(height / GRID_CELL_SIZE)
    GRID_COLS = math.ceil(width / GRID_CELL_SIZE)

    grid_rows = int(np.sqrt(NUM_OF_PARTICLES))
    grid_cols = (NUM_OF_PARTICLES + grid_rows - 1) // grid_rows
    grid_gap = PARTICLE_PIXEL_RADIUS * 1.5

    # Adjust grid parameters if there are extra particles
    while grid_rows * grid_cols > NUM_OF_PARTICLES:
        grid_rows -= 1
        grid_cols = (NUM_OF_PARTICLES + grid_rows - 1) // grid_rows

    # Calculate starting positions for the grid (80% of screen dimensions)
    start_x = width * 0.1  # Start from 10% of the width
    start_y = height * 0.1  # Start from 10% of the height

    # Calculate the gap between particles to fit the 80% area
    gap_x = (width * 0.8 - grid_rows // 2 * (PARTICLE_PIXEL_RADIUS + grid_gap)) / (
        grid_rows
    )
    gap_y = (height * 0.8 - grid_cols // 2 * (PARTICLE_PIXEL_RADIUS + grid_gap)) / (
        grid_cols
    )

    # Place particles in the grid with random offsets
    for i in range(grid_rows):
        for j in range(grid_cols):
            pos = pygame.Vector2()
            pos.x = (
                start_x + i * (PARTICLE_PIXEL_RADIUS + gap_x) + random.uniform(-10, 10)
            )  # Add random offset
            pos.y = (
                start_y + j * (PARTICLE_PIXEL_RADIUS + gap_y) + random.uniform(-10, 10)
            )  # Add random offset
            
            cell_x = int(pos.x // GRID_CELL_SIZE)
            cell_y = int(pos.y // GRID_CELL_SIZE)
            
            p = particle.Particle(
                pos,
                pygame.Vector2(0),
                GREEN,
                PARTICLE_PIXEL_RADIUS,
                DAMPENING_EFFECT,
                (cell_x, cell_y),
            )
            new_particles[cell_x][cell_y].append(p)



def main():
    global new_particles
    run = True
    simcount = 0

    setup()

    while run:
        # clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                new_particles = create_particle_grid()
                setup()
        dt = 0.0003
        simulate(dt)
        if simcount % 10 == 0:
            render()
        simcount += 1


if __name__ == "__main__":
    main()
