import pygame

pygame.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 60


WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, pygame.NOFRAME)
pygame.display.set_caption("PCFD")

def draw():
    pass




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