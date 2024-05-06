import pygame
import numpy as np
import particle
import grid
import time
import random
import math
from space import (
    get_key_from_hash,
    hash_cell,
    position_to_cell_coord,
    update_spatial_lookup,
)

import line_profiler
# kernprof -l .\main.py
# python.exe -m line_profiler .\main.py.lprof

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 1000
NUM_OF_PARTICLES = 300
DAMPENING_EFFECT = 0.75
NEAR_DISTANCE_REQUIRED = 15  # Pixels
PARTICLE_PIXEL_RADIUS = 3.5
REPULSION_COEFF = 1E3
REPULSION_DROPOFF = 6E-2
GRAVITY = pygame.Vector2(0, 9.81 * 1e4)
GRID_CELL_SIZE = 2 * NEAR_DISTANCE_REQUIRED

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

forces = []
start_indices = []
spatial_lookup = []
particles = []


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



def force(cur_particle: particle.Particle, sel_particle: particle.Particle) -> pygame.Vector2:
    f = pygame.Vector2(0)
    
    diff = cur_particle.position - sel_particle.position

    distance = diff.length()

    if distance == 0:
        return pygame.Vector2(0)

    direction = diff.normalize()
    
    f += repulsion(distance, direction)
    f += viscosity(cur_particle, sel_particle, distance)

    return f



def repulsion(distance, direction) -> pygame.Vector2:
    repulsion_force = pygame.Vector2(0)

    force_magnitude = REPULSION_COEFF / ((distance) * REPULSION_DROPOFF) ** 2

    repulsion_force -= direction * force_magnitude

    return repulsion_force



def viscosity(
    cur_particle: particle.Particle, sel_particle: particle.Particle, distance
) -> pygame.Vector2:
    viscosity_force = pygame.Vector2(0)

    viscosity_force = (cur_particle.velocity - sel_particle.velocity) * (
        3 / (distance / PARTICLE_PIXEL_RADIUS)**2
    )

    return viscosity_force


########



def for_each_point_within_radius(particle):
    radius = 15
    center_x, center_y = position_to_cell_coord(particle, radius)
    sqr_radius = radius**2

    for offset_x, offset_y in OFFSETS2D:
        key = get_key_from_hash(
            hash_cell(center_x + offset_x, center_y + offset_y), spatial_lookup
        )
        cell_start_index = start_indices[key]
        forces = pygame.Vector2(0)

        for i in range(cell_start_index, len(spatial_lookup)):
            if spatial_lookup[i].cell_key != key:
                break

            particle_index = spatial_lookup[i].particle_index
            sqr_distance = (
                particles[particle_index].position - particle.position
            ).magnitude_squared()

            forces += GRAVITY
            if sqr_distance <= sqr_radius:
                forces += force(particles[particle_index], particle)

        return forces


def simulate(dt):
    WIN.fill((0, 0, 0))
    update_spatial_lookup(
        particles, NEAR_DISTANCE_REQUIRED, spatial_lookup, start_indices
    )

    for i in range(len(particles)):
        # forces[i] = force(particles[i])
        forces[i] = for_each_point_within_radius(particles[i])
        # if forces[i].x != 0 or forces[i].y != 0:
        # print(forces[i], i, particles[i])

    for i in range(len(particles)):
        particles[i].velocity += forces[i] * dt
        particles[i].position += particles[i].velocity * dt



def render():
    for p in particles:
        p.draw(WIN)

    pygame.display.flip()



def setup():
    width, height = pygame.display.get_window_size()

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
            particles.append(p)
            spatial_lookup.append(987654321)
            start_indices.append(987654321)
            forces.append(pygame.Vector2(0))



def main():
    global particles, spatial_lookup, start_indices
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
                particles = []
                spatial_lookup = []
                start_indices = []
                setup()
        dt = 0.0001
        simulate(dt)
        if simcount % 10 == 0:
            render()
        simcount += 1


if __name__ == "__main__":
    main()
