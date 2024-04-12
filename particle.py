import pygame
import numpy as np


class Particle:
    def __init__(
        self,
        x: int,
        y: int,
        color: tuple,
        velocity: pygame.Vector2,
        size: int,
        dampening_effect: float,
    ):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.size = size
        self.dampening_effect = -dampening_effect

    def draw(self, window):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        win_width, win_height = window.get_size()

        # Check if particle touches left or right boundary
        if self.x - self.size <= 0 or self.x + self.size >= win_width:
            self.velocity[0] *= self.dampening_effect

        # Check if particle touches top or bottom boundary
        if self.y - self.size <= 0 or self.y + self.size >= win_height:
            self.velocity[1] *= self.dampening_effect

        # Make sure the particles are inside the bounding box, which is set to the window size.
        self.x = max(self.size, min(self.x, win_width - self.size))
        self.y = max(self.size, min(self.y, win_height - self.size))

        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)
