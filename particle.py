import pygame

class Particle:
    def __init__(self, x, y, color, velocity):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
    
    def draw(self, window, size):
        pygame.draw.circle(window, self.color, (self.x, self.y), size)