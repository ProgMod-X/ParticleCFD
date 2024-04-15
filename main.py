import pygame
import numpy as np
import particle
import time
import random

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 120
NUM_OF_PARTICLES = 20
DAMPENING_EFFECT = .75
NEAR_DISTANCE_REQUIRED = 50 # Pixels
PARTICLE_PIXEL_RADIUS = 7
PARTICLE_METER_RADIUS = 0.1 # Meter
GRAVITY = 9.81
IRL_GRAVITY = pygame.Vector2()
IRL_GRAVITY.y = GRAVITY*(PARTICLE_PIXEL_RADIUS/PARTICLE_METER_RADIUS)

# Colors
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("PCFD")

particle_list = []
last_particle_list = []

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

def repulsion(cur_particle: particle.Particle) -> pygame.Vector2:
    global last_particle_list

    repulsion_force = pygame.Vector2()
    for sel_particle in last_particle_list:
        if sel_particle == cur_particle:
            continue
        
        diff = sel_particle.position - cur_particle.position
        distance = diff.length() - 2 * PARTICLE_PIXEL_RADIUS

        if distance == 0 or diff == [0, 0]:
            #print("overlap")
            continue
        
        # Calculate normalized direction vector with length 1
        direction = diff.normalize()
    
        # Calculate the force magnitude based on distance
        force_magnitude = 1E5 / (distance)**2 # Inverse square law
    
        repulsion_force -= direction * force_magnitude
        
    return repulsion_force  


def simulate(dt):
    global particle_list
    global last_particle_list

    last_particle_list = [p for p in particle_list]
    particle_list = []
    WIN.fill((0, 0, 0))
    for cur_particle in last_particle_list:
        # Calculate the new position and velocity based on the forces
        new_velocity = cur_particle.velocity + (force(IRL_GRAVITY, cur_particle)) * dt
        new_position = cur_particle.position + (cur_particle.velocity) * dt
        
        # Create a new Particle instance with the updated properties
        current_particle = particle.Particle(new_position, new_velocity, GREEN, PARTICLE_PIXEL_RADIUS, DAMPENING_EFFECT)
        
        # Add the updated particle to the new particle_list
        particle_list.append(current_particle)
        
        # Draw the updated particle
        current_particle.draw(WIN)
    
    pygame.display.flip()




def setup():
    global last_particle_list

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
            particle_list.append(particle.Particle(pos, pygame.Vector2(0), GREEN, PARTICLE_PIXEL_RADIUS, DAMPENING_EFFECT))
    
    last_particle_list = particle_list



def main():
    global WIN
    global particle_list
    global last_particle_list

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
        dt = 0.01
        simulate(dt)

if __name__ == "__main__":
    main()