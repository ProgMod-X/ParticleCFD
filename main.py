import pygame

pygame.init()

WIDTH, HEIGHT = 400, 400
FPS = 60
NUM_OF_PARTICLES = 10
PARTICLE_SIZE = 5

# Colors
GREEN = (0, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("PCFD")

def draw():
    pygame.draw.circle(WIN, GREEN, (WIDTH/2, HEIGHT/2), PARTICLE_SIZE)
    pygame.display.flip()

def main():
    run = True
    clock = pygame.time.Clock()

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