import pygame
import numpy as np
import particle
import time

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 60
NUM_OF_PARTICLES = 21
DAMPENING_EFFECT = 1
PARTICLE_PIXEL_RADIUS = 10
PARTICLE_METER_RADIUS = 10 # Meter
GRAVITY = 9.81
IRL_GRAVITY = pygame.Vector2()
IRL_GRAVITY.y = GRAVITY*(PARTICLE_PIXEL_RADIUS/PARTICLE_METER_RADIUS)

# Colors
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("PCFD")

def deltaTime():
    # Get the current time in seconds
    current_time = time.time()
    
    # Calculate the difference between the current time and the last time deltaTime was called
    if 'last_time' not in deltaTime.__dict__:
        deltaTime.last_time = current_time
    delta_time = current_time - deltaTime.last_time
    
    # Update the last_time for the next deltaTime call
    deltaTime.last_time = current_time
    
    return delta_time

def force(GRAVITY, particles):
    force = GRAVITY
    #force += repulsion(particles)
    
    return force


particle_list = []

def draw(dt):
    WIN.fill((0, 0, 0))
    for particle in particle_list:
        particle.velocity += force(IRL_GRAVITY, particle_list)*dt
        particle.draw(WIN)

    
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

    # Calculate starting positions for the grid
    start_x = width // 2 - (grid_rows // 2) * (PARTICLE_PIXEL_RADIUS + grid_gap)
    start_y = height // 2 - (grid_cols // 2) * (PARTICLE_PIXEL_RADIUS + grid_gap)

    # Place particles in the grid
    for i in range(grid_rows):
        for j in range(grid_cols):
            x = start_x + i * (PARTICLE_PIXEL_RADIUS + grid_gap)
            y = start_y + j * (PARTICLE_PIXEL_RADIUS + grid_gap)
            particle_list.append(particle.Particle(x, y, GREEN, pygame.Vector2(0), PARTICLE_PIXEL_RADIUS, DAMPENING_EFFECT))


def main():
    global WIN
    global particle_list

    run = True
    clock = pygame.time.Clock()

    setup()

    while run:
        clock.tick(FPS)
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
        dt = deltaTime()
        draw(dt)

if __name__ == "__main__":
    main()