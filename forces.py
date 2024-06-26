from particle import Particle
from pygame import Vector2, mouse
import math

def calculate_forces(iter_particle: Particle, particle: Particle, near_distance_required, repulsion_coeff, repulsion_dropoff, particle_pixel_radius, viscosity_const) -> Vector2:
    f = Vector2(0)
    
    diff = iter_particle.position - particle.position

    distance = diff.length()

    if distance == 0 or distance > near_distance_required:
        return f

    diff.normalize_ip()
    
    f += repulsion(distance, diff, repulsion_coeff, repulsion_dropoff)
    f += viscosity(iter_particle, particle, distance, particle_pixel_radius, viscosity_const)

    return f



def repulsion(distance, direction, repulsion_coeff, repulsion_dropoff) -> Vector2:
    force_magnitude = repulsion_coeff / (distance * repulsion_dropoff) ** 2

    repulsion_force = direction * force_magnitude
    repulsion_force *= -1

    return repulsion_force

def viscosity(iter_particle: Particle, particle: Particle, distance, particle_pixel_radius, viscosity_const) -> Vector2:
    viscosity_force = (iter_particle.velocity - particle.velocity) * (1 / ((distance / particle_pixel_radius)* 1/viscosity_const)**2)
    return viscosity_force

def mouse_force(particle: Particle, diff, distance, near_distance_required, particle_pixel_radius, mouse_repulsion_coeff, mouse_repulsion_dropoff, left_click, right_click) -> Vector2:
    direction = diff.normalize()
    
    if left_click:  # Left click: Repulsion
        force_magnitude = mouse_repulsion_coeff / ((distance) * mouse_repulsion_dropoff) ** 2
        repulsion_force = -direction * force_magnitude  
        return repulsion_force

    elif right_click:  # Right click: Attraction
        force_magnitude = (math.e * distance) / (math.exp(distance/particle_pixel_radius)) * 1E5
        attraction_force = direction * force_magnitude
        return attraction_force
    
    else:  # No click: No force
        return Vector2(0)