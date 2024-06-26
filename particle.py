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

    def update(self, window):
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

    def draw(self, window):
        color_value = self.colorvalue()

        if color_value == 1000:
            color_r = 255
            color_g = 0
            color_b = 0
        elif color_value > 255:
            color_r = 255
            color_g = 510 - self.colorvalue() 
            color_b = 0
        else:
            color_r = color_value
            color_g = color_value
            if color_value < 127.5:
                color_b = 255 - color_value*2
            else:
                color_b = 0

        self.color = (color_r, color_g, color_b)

        pygame.draw.circle(window, self.color, self.position.xy, self.size)
    
    def colorvalue(self):
        a = 0.5 * self.velocity.length()
        if a > 1000:
            a = 1000
        elif a > 510:
            a = 510
        elif a < 0:
            a = 0
        return a