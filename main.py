import pygame
import particle

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 60
NUM_OF_PARTICLES = 10
PARTICLE_SIZE = 5

# Colors
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("PCFD")

particle_list = []

def draw():
    for particle in particle_list:
        particle.draw(WIN, PARTICLE_SIZE)


def setup():
    for i in range(NUM_OF_PARTICLES):
        particle_list.append(particle.Particle(0, PARTICLE_SIZE, GREEN, 0))


def main():
    run = True
    clock = pygame.time.Clock()

    setup()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
        draw()

if __name__ == "__main__":
    main()