import pygame
import numpy as np

class Particle:
    def __init__(self, x, y, color, velocity):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
    
    def draw(self, window, size):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        pygame.draw.circle(window, self.color, (self.x, self.y), size)