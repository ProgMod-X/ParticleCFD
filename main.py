import pygame
import numpy as np
import particle

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 60
NUM_OF_PARTICLES = 21
PARTICLE_SIZE = 10
GRAVITY = 9.81

# Colors
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("PCFD")

particle_list = []

def draw():
    WIN.fill((0, 0, 0))
    for particle in particle_list:
        particle.draw(WIN, PARTICLE_SIZE)

    
    pygame.display.flip()


def setup():

    width, height = pygame.display.get_window_size()

    grid_rows = int(np.sqrt(NUM_OF_PARTICLES))
    grid_cols = (NUM_OF_PARTICLES + grid_rows - 1) // grid_rows
    grid_gap = PARTICLE_SIZE * 1.5

    # Adjust grid parameters if there are extra particles
    while grid_rows * grid_cols > NUM_OF_PARTICLES:
        grid_rows -= 1
        grid_cols = (NUM_OF_PARTICLES + grid_rows - 1) // grid_rows

    # Calculate starting positions for the grid
    start_x = width // 2 - (grid_rows // 2) * (PARTICLE_SIZE + grid_gap)
    start_y = height // 2 - (grid_cols // 2) * (PARTICLE_SIZE + grid_gap)

    # Place particles in the grid
    for i in range(grid_rows):
        for j in range(grid_cols):
            x = start_x + i * (PARTICLE_SIZE + grid_gap)
            y = start_y + j * (PARTICLE_SIZE + grid_gap)
            particle_list.append(particle.Particle(x, y, GREEN, np.array([0, GRAVITY])))


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
        draw()

if __name__ == "__main__":
    main()