import pygame
import numpy as np
import particle
import time

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 5
NUM_OF_PARTICLES = 2
DAMPENING_EFFECT = .97
NEAR_DISTANCE_REQUIRED = 20
PARTICLE_PIXEL_RADIUS = 10
PARTICLE_METER_RADIUS = 10 # Meter
GRAVITY = 9.81
IRL_GRAVITY = pygame.Vector2()
IRL_GRAVITY.y = GRAVITY*(PARTICLE_PIXEL_RADIUS/PARTICLE_METER_RADIUS)

# Colors
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("PCFD")

particle_list = []

def deltaTime() -> float:
    # Get the current time in seconds
    current_time = time.time()
    
    # Calculate the difference between the current time and the last time deltaTime was called
    if 'last_time' not in deltaTime.__dict__:
        deltaTime.last_time = current_time
    delta_time = current_time - deltaTime.last_time
    
    # Update the last_time for the next deltaTime call
    deltaTime.last_time = current_time
    
    return delta_time

def force(gravity: pygame.Vector2, particle: particle.Particle) -> pygame.Vector2:
    force = gravity
    force += repulsion(particle)
    
    return force

def repulsion(particle: particle.Particle) -> pygame.Vector2:
    repulsion_force = pygame.Vector2()
    for sel_particle in particle_list:
        if sel_particle == particle:
            continue
        angle = particle.position.angle_to(sel_particle.position)
        distance = particle.position.distance_to(sel_particle.position)
        
        force = 0 if distance == 0 else 1 / distance


        repulsion_force.x += np.cos(angle) * force
        repulsion_force.y += np.sin(angle) * force
    return repulsion_force

def draw(dt):
    WIN.fill((0, 0, 0))
    for particle in particle_list:
        particle.velocity += force(IRL_GRAVITY, particle)*dt
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
            pos = pygame.Vector2()
            pos.x = start_x + i * (PARTICLE_PIXEL_RADIUS + grid_gap)
            pos.y = start_y + j * (PARTICLE_PIXEL_RADIUS + grid_gap)
            particle_list.append(particle.Particle(pos, GREEN, pygame.Vector2(0), PARTICLE_PIXEL_RADIUS, DAMPENING_EFFECT))


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