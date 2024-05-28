import pygame
import numpy as np

class Particle:
    def __init__(
        self,
        posistion,
        velocity,
        color: tuple,
        size: int,
        dampening_effect: float,
        cell,
    ):
        self.position = posistion
        self.color = color
        self.velocity = velocity
        self.size = size
        self.dampening_effect = -dampening_effect
        self.cell = cell

    def draw(self, window):
        win_width, win_height = window.get_size()

        # Check if particle touches left or right boundary
        if self.position[0] - self.size <= 0 or self.position[0] + self.size >= win_width:
            self.velocity[0] *= self.dampening_effect

        # Check if particle touches top or bottom boundary
        if self.position[1] - self.size <= 0 or self.position[1] + self.size >= win_height:
            self.velocity[1] *= self.dampening_effect

        # Make sure the particles are inside the bounding box, which is set to the window size.
        self.position[0] = max(self.size, min(self.position[0], win_width - self.size))
        self.position[1] = max(self.size, min(self.position[1], win_height - self.size))

        color_value = self.colorvalue(self.velocity[0], self.velocity[1])

        if color_value == 1000:
            color_r = 255
            color_g = 25
            color_b = 255
        elif color_value > 255:
            color_r = 255
            color_g = 510 -self.colorvalue(self.velocity[0], self.velocity[1]) 
            color_b = 0
        else:
            color_r = color_value
            color_g = color_value
            if color_value < 127.5:
                color_b = 255 - color_value*2
            else:
                color_b = 0

        self.color = (color_r, color_g, color_b)

        pygame.draw.circle(window, self.color, self.position, self.size)
    
    def colorvalue(self, x, y):
        a = 0.5 * (np.sqrt(x**2 + y**2))
        if a > 1000:
            a = 1000
        elif a > 510:
            a = 510
        elif a < 0:
            a = 0
        return a