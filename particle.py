import pygame
import numpy as np


class Particle:
    def __init__(
        self,
        posistion: pygame.Vector2,
        color: tuple,
        velocity: pygame.Vector2,
        size: int,
        dampening_effect: float,
    ):
        self.position = posistion
        self.color = color
        self.velocity = velocity
        self.size = size
        self.dampening_effect = -dampening_effect

    def draw(self, window, dt):
        self.position += self.velocity*dt

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

        pygame.draw.circle(window, self.color, self.position.xy, self.size)
