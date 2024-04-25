import pygame
import numpy as np
import particle
import grid
import time
import random
import math

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 1000
NUM_OF_PARTICLES = 250
DAMPENING_EFFECT = 0.75
NEAR_DISTANCE_REQUIRED = 25  # Pixels
PARTICLE_PIXEL_RADIUS = 4
PARTICLE_METER_RADIUS = 0.1  # Meter
FORCE_COEFFICIENT = (PARTICLE_PIXEL_RADIUS / PARTICLE_METER_RADIUS)
REPULSION_COEFF = 1E8
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


def force(particle: particle.Particle) -> pygame.Vector2:
    f = pygame.Vector2(0)
    f += GRAVITY
    f += repulsion(particle)
    f += viscosity(particle)

    return f


def repulsion(sel_particle: particle.Particle) -> pygame.Vector2:
    particle_list = particle_grid.get_neighbours(sel_particle)
    
    repulsion_force = pygame.Vector2(0)

    for cur_particle in particle_list:
        if cur_particle == sel_particle:
            continue

        diff = cur_particle.position - sel_particle.position

        distance = diff.length()

        if distance != 0:
            force_magnitude = REPULSION_COEFF / (distance * (FORCE_COEFFICIENT * 5E-1))**2
        else:
            force_magnitude = REPULSION_COEFF * cur_particle.velocity.normalize()
            repulsion_force -= force_magnitude
            continue

        direction = diff.normalize()

        repulsion_force -= direction * force_magnitude

    return repulsion_force

def viscosity(sel_particle: particle.Particle) -> pygame.Vector2:
    particle_list = particle_grid.get_neighbours(sel_particle)

    viscosity_force = pygame.Vector2(0)

    for cur_particle in particle_list:
        if cur_particle == sel_particle:
            continue

        diff = cur_particle.position - sel_particle.position

        distance = diff.length()

        if distance != 0:
            viscosity_force = (cur_particle.velocity - sel_particle.velocity) * (7E0 / ((distance - PARTICLE_PIXEL_RADIUS)/PARTICLE_PIXEL_RADIUS))
        else:
            viscosity_force = (cur_particle.velocity - sel_particle.velocity)

    return viscosity_force

def simulate(dt):
    WIN.fill((0, 0, 0))
    particles = particle_grid.get_all_particles()

    # print(forces)
    for i in range(len(particles)):
        forces[i] = force(particles[i])

    for i in range(len(particles)):
        particles[i].velocity += forces[i] * dt
        particles[i].position += particles[i].velocity * dt

    for i in range(len(particles)):
        particle_grid.remove_particle(particles[i])
        particle_grid.add_particle(particles[i])


def render():
    particles = particle_grid.get_all_particles()

    for p in particles:
        p.draw(WIN)

    pygame.display.flip()


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

    # Calculate starting positions for the grid
    start_x = width // 2 - (grid_rows // 2) * (PARTICLE_PIXEL_RADIUS + grid_gap)
    start_y = height // 2 - (grid_cols // 2) * (PARTICLE_PIXEL_RADIUS + grid_gap)

    # Place particles in the grid with random offsets
    for i in range(grid_rows):
        for j in range(grid_cols):
            pos = pygame.Vector2()
            pos.x = (
                start_x
                + i * (PARTICLE_PIXEL_RADIUS + grid_gap)
                + random.uniform(-10, 10)
            )  # Add random offset
            pos.y = (
                start_y
                + j * (PARTICLE_PIXEL_RADIUS + grid_gap)
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
        dt = 0.0001
        simulate(dt)
        if simcount % 10 == 0:
            render()
        simcount += 1


if __name__ == "__main__":
    main()
