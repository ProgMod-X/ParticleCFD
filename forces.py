from particle import Particle
from pygame import mouse

import os
os.environ["JAX_PLATFORM_NAME"] = "cpu"
import jax.numpy as np

import line_profiler
from numba import jit

#@line_profiler.profile                
def calculate_forces(iter_particle: Particle, particle: Particle, near_distance_required, repulsion_coeff, repulsion_dropoff, particle_pixel_radius, viscosity_const):
    f = np.array([0.0, 0.0])
    
    diff = iter_particle.position - particle.position
    distance = np.linalg.norm(diff)
    
    if distance == 0 or distance > near_distance_required:
        return f
    
    direction = diff / distance

    f = f.at[:].add(repulsion(distance, direction, repulsion_coeff, repulsion_dropoff))
    
    vel_diff = iter_particle.velocity - particle.velocity
    
    f = f.at[:].add(viscosity(vel_diff, distance, direction, particle_pixel_radius, viscosity_const))

    return f

#@line_profiler.profile            
def repulsion(distance, direction, repulsion_coeff, repulsion_dropoff):
    force_magnitude = repulsion_coeff / (distance * repulsion_dropoff) ** 2
    return -direction * force_magnitude

def mouse_force(particle: Particle, near_distance_required, particle_pixel_radius, mouse_repulsion_coeff, mouse_repulsion_dropoff):
    mouse_pos = mouse.get_pos()  
    left_click, middle_click, right_click = mouse.get_pressed()
    if not (left_click or right_click):
        return np.array([0.0, 0.0])

    diff = np.array([mouse_pos[0] - particle.position[0], mouse_pos[1] - particle.position[1]])
    distance = np.sqrt(diff[0] ** 2 + diff[1] ** 2)
    direction = diff / distance

    if distance == 0 or distance > near_distance_required*3:
        return np.array([0.0, 0.0])

    if left_click:  # Left click: Repulsion
        force_magnitude = mouse_repulsion_coeff / ((distance) * mouse_repulsion_dropoff) ** 2
        return -direction * force_magnitude

    elif right_click:  # Right click: Attraction
        force_magnitude = (np.e * distance) / (np.exp(distance/particle_pixel_radius)) * 1E5
        return direction * force_magnitude
    
    else:  # No click: No force
        return np.array([0.0, 0.0])

#@line_profiler.profile            
def viscosity(vel_diff, distance, direction, particle_pixel_radius, viscosity_const):
    return vel_diff * (particle_pixel_radius * viscosity_const / distance) ** 2