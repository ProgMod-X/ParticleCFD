import pygame
import numpy as np
import particle
import grid
import time
import random
import math

import line_profiler
# kernprof -l .\main.py
# python.exe -m line_profiler .\main.py.lprof

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 1000
NUM_OF_PARTICLES = 200
DAMPENING_EFFECT = 0.75
NEAR_DISTANCE_REQUIRED = 9  # Pixels
PARTICLE_PIXEL_RADIUS = 3
PARTICLE_METER_RADIUS = 0.1  # Meter
FORCE_COEFFICIENT = (PARTICLE_PIXEL_RADIUS / PARTICLE_METER_RADIUS)
REPULSION_COEFF = 1E9
GRAVITY = pygame.Vector2(0, 9.81*1E4) / FORCE_COEFFICIENT
GRID_CELL_SIZE = 2 * NEAR_DISTANCE_REQUIRED

# Colors
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("PCFD")

particle_grid = grid.Grid(WIDTH, HEIGHT, GRID_CELL_SIZE)
forces = []


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


@line_profiler.profile
def force(particle: particle.Particle) -> pygame.Vector2:
    particle_list = particle_grid.get_neighbours(particle)
    f = pygame.Vector2(0)
    f += GRAVITY
    
    for cur_particle in particle_list:
        if cur_particle == particle:
            continue

        diff = cur_particle.position - particle.position
        distance = diff.length()
        
        f += repulsion(diff, distance)
        f += viscosity(particle, cur_particle, distance)

    return f


def repulsion(diff, distance) -> pygame.Vector2:
    repulsion_force = pygame.Vector2(0)

    if distance != 0:
        force_magnitude = REPULSION_COEFF / ((distance) * (FORCE_COEFFICIENT * 2))**2

    direction = diff.normalize()

    repulsion_force -= direction * force_magnitude

    return repulsion_force

@line_profiler.profile
def viscosity(sel_particle: particle.Particle, cur_particle, distance) -> pygame.Vector2:
    viscosity_force = pygame.Vector2(0)
    
    if distance != 0:
        viscosity_force = (cur_particle.velocity - sel_particle.velocity) * (1 / ((distance)/PARTICLE_PIXEL_RADIUS))

    return viscosity_force

@line_profiler.profile
def simulate(dt):
    WIN.fill((0, 0, 0))
    particles = particle_grid.get_all_particles()

    # print(forces)
    for i in range(len(particles)):
        forces[i] = force(particles[i])

    for i in range(len(particles)):
        particles[i].velocity += forces[i] * dt
        particles[i].position += particles[i].velocity * dt
        particle_grid.remove_particle(particles[i])
        particle_grid.add_particle(particles[i])


@line_profiler.profile
def render():
    particles = particle_grid.get_all_particles()

    for p in particles:
        p.draw(WIN)

    pygame.display.flip()


@line_profiler.profile
def setup():
    global particle_grid

    width, height = pygame.display.get_window_size()
    particle_grid = grid.Grid(width, height, GRID_CELL_SIZE)

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
    gap_x = (width * 0.8 - grid_rows // 2 * (PARTICLE_PIXEL_RADIUS + grid_gap)) / (grid_rows)
    gap_y = (height * 0.8 - grid_cols // 2 * (PARTICLE_PIXEL_RADIUS + grid_gap)) / (grid_cols)

    # Place particles in the grid with random offsets
    for i in range(grid_rows):
        for j in range(grid_cols):
            pos = pygame.Vector2()
            pos.x = (
                start_x
                + i * (PARTICLE_PIXEL_RADIUS + gap_x)
                + random.uniform(-10, 10)
            )  # Add random offset
            pos.y = (
                start_y
                + j * (PARTICLE_PIXEL_RADIUS + gap_y)
                + random.uniform(-10, 10)
            )  # Add random offset
            p = particle.Particle(
                pos,
                pygame.Vector2(0),
                GREEN,
                PARTICLE_PIXEL_RADIUS,
                DAMPENING_EFFECT,
                (
                    math.floor(pos.x / GRID_CELL_SIZE),
                    math.floor(pos.y / GRID_CELL_SIZE),
                ),
            )
            particle_grid.add_particle(p)
            forces.append(pygame.Vector2(0))

@line_profiler.profile
def main():
    global particle_grid

    run = True
    clock = pygame.time.Clock()
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
                particle_grid = None
                setup()
        dt = 0.0004
        simulate(dt)
        if simcount % 10 == 0:
            render()
        simcount += 1


if __name__ == "__main__":
    main()
