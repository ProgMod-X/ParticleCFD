import pygame
import numpy as np
import particle
import time
import random

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 100
NUM_OF_PARTICLES = 50
DAMPENING_EFFECT = 0.75
NEAR_DISTANCE_REQUIRED = 30  # Pixels
PARTICLE_PIXEL_RADIUS = 4
PARTICLE_METER_RADIUS = 0.1  # Meter
FORCE_COEFFICIENT = (PARTICLE_PIXEL_RADIUS / PARTICLE_METER_RADIUS)
REPULSION_COEFF = 1E8
GRAVITY = pygame.Vector2(0, 9.81*1E4) / FORCE_COEFFICIENT

# Colors
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("PCFD")

particle_list = []
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
    global particle_list

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
    global particle_list

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

    # print(forces)
    for i in range(len(particle_list)):
        forces[i] = force(particle_list[i])

    for i in range(len(particle_list)):
        particle_list[i].velocity += forces[i] * dt
        particle_list[i].position += particle_list[i].velocity * dt
        

def render():
    for p in particle_list:
        p.draw(WIN)

    pygame.display.flip()


def setup():
    global particle_list

    width, height = pygame.display.get_window_size()

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
            pos.x = start_x + i * (PARTICLE_PIXEL_RADIUS + grid_gap) + random.uniform(-10, 10) # Add random offset
            pos.y = start_y + j * (PARTICLE_PIXEL_RADIUS + grid_gap) + random.uniform(-10, 10) # Add random offset
            particle_list.append(particle.Particle(pos, pygame.Vector2(0), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), PARTICLE_PIXEL_RADIUS, DAMPENING_EFFECT))
            forces.append(pygame.Vector2(0))


def main():
    global particle_list

    run = True
    clock = pygame.time.Clock()
    simcount = 0

    setup()

    while run:
        #clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                particle_list = []
                setup()
        dt = 0.0001
        simulate(dt)
        if simcount % 10 == 0:
            render()
        simcount += 1


if __name__ == "__main__":
    main()
