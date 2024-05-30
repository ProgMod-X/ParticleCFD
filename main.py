import pygame
import numpy as np
import particle
import time
import random
import math

from forces import calculate_forces, mouse_force
from grid import get_neighbours_3x3, update_cell, create_particle_grid

import line_profiler
# kernprof -l .\main.py
# python.exe -m line_profiler .\main.py.lprof

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 1000

NUM_OF_PARTICLES = 300
NEAR_DISTANCE_REQUIRED = 15  # Pixels
PARTICLE_PIXEL_RADIUS = 3.5

DAMPENING_EFFECT = 0.9

REPULSION_COEFF = 3E3 # Higher value means stronger repulsion
REPULSION_DROPOFF = 6E-2 # Higher value means faster dropoff and less repulsion
MOUSE_REPULSION_COEFF = 1E3
MOUSE_REPULSION_DROPOFF = 1E-2
MOUSE_ATTRACTION_COEFF = 5E4
MOUSE_ATTRACTION_DROPOFF = 7E-2 
VISCOSITY_CONST = 6

GRAVITY = pygame.Vector2(0, 9.81 * 1E3)

GRID_CELL_SIZE = NEAR_DISTANCE_REQUIRED
GRID_ROWS = math.ceil(HEIGHT / GRID_CELL_SIZE)
GRID_COLS = math.ceil(WIDTH / GRID_CELL_SIZE)

# Colors
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("PCFD")

forces = {}

particles = create_particle_grid(GRID_ROWS, GRID_COLS)

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


                
def simulate(dt):
    WIN.fill((0, 0, 0))

    for x in range(GRID_ROWS):
        for y in range(GRID_COLS):
            for particle in particles[x][y]:
                particles[x][y].remove(particle)
                update_cell(particle, GRID_ROWS, GRID_COLS, GRID_CELL_SIZE)
                particles[particle.cell[0]][particle.cell[1]].append(particle)

    for x in range(GRID_ROWS):
        for y in range(GRID_COLS):
            neighbours = get_neighbours_3x3((x, y), GRID_ROWS, GRID_COLS, particles)
            for particle in particles[x][y]:
                f = pygame.Vector2(0)
                f += GRAVITY

                left_click, middle_click, right_click = pygame.mouse.get_pressed()

                if (left_click or right_click):
                    f += mouse_force(particle, NEAR_DISTANCE_REQUIRED, PARTICLE_PIXEL_RADIUS, MOUSE_REPULSION_COEFF, MOUSE_REPULSION_DROPOFF)
                for iter_particle in neighbours:
                    f += calculate_forces(iter_particle, particle, NEAR_DISTANCE_REQUIRED, REPULSION_COEFF, REPULSION_DROPOFF, PARTICLE_PIXEL_RADIUS, VISCOSITY_CONST)


                forces[particle] = f
                
                particle.velocity += forces[particle] * dt
                particle.position += particle.velocity * dt

                particle.update(WIN)



def render():
    for x in range(GRID_ROWS):
        for y in range(GRID_COLS):
            for p in particles[x][y]:
                p.draw(WIN)

    pygame.display.flip()


def setup():
    global GRID_ROWS, GRID_COLS, particles
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
                3 + random.random() * 2,
                DAMPENING_EFFECT,
                (cell_x, cell_y),
            )
            particles[cell_x][cell_y].append(p)



def main():
    global particles
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
                particles = create_particle_grid(GRID_ROWS, GRID_COLS)
                setup()
        dt = 0.0003
        simulate(dt)
        if simcount % 10 == 0:
            render()
        simcount += 1


if __name__ == "__main__":
    main()
