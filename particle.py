import pygame
import numpy as np

class Particle:
    def __init__(self, x, y, color, velocity, size):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.size = size
    
    def draw(self, window):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        win_width, win_height = window.get_size()

        # Make sure the particles are inside the bounding box, which is set to the window size.
        pygame.math.clamp(self.x, self.size, win_width - self.size)
        pygame.math.clamp(self.y, self.size, win_height - self.size)

        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)