from particle import Particle
from pygame import Vector2, mouse
import math

def calculate_forces(iter_particle: Particle, particle: Particle, near_distance_required, repulsion_coeff, repulsion_dropoff, particle_pixel_radius, viscosity_const) -> Vector2:
    f = Vector2(0)
    
    diff = iter_particle.position - particle.position

    distance = diff.length()

    if distance == 0 or distance > near_distance_required:
        return f

    direction = diff.normalize()
    
    f += repulsion(distance, direction, repulsion_coeff, repulsion_dropoff)
    f += viscosity(iter_particle, particle, distance, particle_pixel_radius, viscosity_const)

    return f



def repulsion(distance, direction, repulsion_coeff, repulsion_dropoff) -> Vector2:
    repulsion_force = Vector2(0)

    force_magnitude = repulsion_coeff / ((distance) * repulsion_dropoff) ** 2

    repulsion_force -= direction * force_magnitude

    return repulsion_force

def mouse_force(particle: Particle, near_distance_required, particle_pixel_radius, mouse_repulsion_coeff, mouse_repulsion_dropoff) -> Vector2:
    mouse_pos = mouse.get_pos()  
    left_click, middle_click, right_click = mouse.get_pressed()

    if not (left_click or right_click):
        return Vector2(0)

    if left_click:  # Left click: Repulsion
        diff = Vector2(mouse_pos) - particle.position
        distance = diff.length()
        direction = diff.normalize()
        
        if distance == 0 or distance > near_distance_required*3:
            return Vector2(0)
        
        force_magnitude = mouse_repulsion_coeff / ((distance) * mouse_repulsion_dropoff) ** 2
        repulsion_force = -direction * force_magnitude  
        return repulsion_force

    elif right_click:  # Right click: Attraction
        diff = Vector2(mouse_pos) - particle.position
        distance = diff.length()
        direction = diff.normalize()

        if distance == 0 or distance > near_distance_required*3:
            return Vector2(0)
 
        force_magnitude = (math.e * distance) / (math.exp(distance/particle_pixel_radius)) * 1E5
        attraction_force = direction * force_magnitude
        return attraction_force
    
    else:  # No click: No force
        return Vector2(0)

def viscosity(iter_particle: Particle, particle: Particle, distance, particle_pixel_radius, viscosity_const) -> Vector2:
    viscosity_force = Vector2(0)

    viscosity_force = (iter_particle.velocity - particle.velocity) * (
        1 / ((distance / particle_pixel_radius)* 1/viscosity_const)**2
    )

    return viscosity_force
