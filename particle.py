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
        if self.position.x - self.size <= 0 or self.position.x + self.size >= win_width:
            self.velocity.x *= self.dampening_effect

        # Check if particle touches top or bottom boundary
        if self.position.y - self.size <= 0 or self.position.y + self.size >= win_height:
            self.velocity.y *= self.dampening_effect

        # Make sure the particles are inside the bounding box, which is set to the window size.
        self.position.x = max(self.size, min(self.position.x, win_width - self.size))
        self.position.y = max(self.size, min(self.position.y, win_height - self.size))

        if self.colorvalue(self.velocity.x, self.velocity.y) == 1000:
            color_r = 255
            color_g = 255
            color_b = 255
        elif self.colorvalue(self.velocity.x, self.velocity.y) > 255:
            color_r = 255
            color_g = 510 -self.colorvalue(self.velocity.x, self.velocity.y) 
            color_b = 0
        else:
            color_r = self.colorvalue(self.velocity.x, self.velocity.y)
            color_g = self.colorvalue(self.velocity.x, self.velocity.y)
            if self.colorvalue(self.velocity.x, self.velocity.y) < 127.5:
                color_b = 255 - self.colorvalue(self.velocity.x, self.velocity.y)*2
            else:
                color_b = 0

        self.color = (color_r, color_g, color_b)

        pygame.draw.circle(window, self.color, self.position.xy, self.size)
    
    def colorvalue(self, x, y):
        a = 0.3 * (math.sqrt(x**2 + y**2))
        if a > 1000:
            a = 1000
        elif a > 510:
            a = 510
        elif a < 0:
            a = 0
        return a