import pygame
import numpy as np
import math

class Particle:
    def __init__(
        self,
        posistion: pygame.Vector2,
        velocity: pygame.Vector2,
        color: tuple,
        size: int,
        dampening_effect: float,
        grid_cell
    ):
        self.position = posistion
        self.color = color
        self.velocity = velocity
        self.size = size
        self.dampening_effect = -dampening_effect
        self.grid_cell = grid_cell

    def draw(self, window):
        win_width, win_height = window.get_size()

        # Check if particle touches left or right boundary
        if self.position.x - self.size <= 0 or self.position.x + self.size >= win_width:
            self.velocity.x *= self.dampening_effect

        # Check if particle touches top or bottom boundary
        if self.position.y - self.size <= 0 or self.position.y + self.size >= win_height:
            self.velocity.y *= self.dampening_effect

        # Make sure the particles are inside the bounding box, which is set to the window size.
        self.position.x = max(self.size, min(self.position.x, win_width - self.size))
        self.position.y = max(self.size, min(self.position.y, win_height - self.size))

        color_1 = self.collourvalue(self.velocity.x, self.velocity.y)

        self.color = (color_1, 255 - self.collourvalue(self.velocity.x, self.velocity.y), 0)

        pygame.draw.circle(window, self.color, self.position.xy, self.size)
    
    def colorvalue(self, x, y):
        a =  0.40 * (math.sqrt(x**2 + y**2))
        if a > 255:
            a = 255
        elif a < 1:
            a = 1
        return a