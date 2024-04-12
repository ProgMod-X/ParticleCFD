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

        # The below is the first iteration of the bounding box
        # if self.x < 0:
        #     self.x = 0 + self.size
        # elif self.x > win_width:
        #     self.x = win_width - self.size
        # if self.y < 0:
        #     self.y = 0 + self.size
        # elif self.y > win_height:
        #     self.y = win_height - self.size

        # Make sure the particles are inside the bounding box, which is set to the window size.
        self.x = max(self.size, min(self.x, win_width - self.size))
        self.y = max(self.size, min(self.y, win_height - self.size))

        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)