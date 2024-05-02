import numpy as np
import line_profiler

class SpatialEntry:
    def __init__(self, i, cell_key) -> None:
        self.particle_index = i
        self.cell_key = cell_key

    def __lt__(self, other):
        if not isinstance(other, SpatialEntry):
            raise TypeError("'<' not supported between instances of 'SpatialEntry' and '{}'".format(type(other)))
        return (self.cell_key) < (other.cell_key)


def update_spatial_lookup(particles, radius, spatial_lookup, start_indices):

    for i in range(len(particles)):
        cell_x, cell_y = position_to_cell_coord(particles[i], radius)
        cell_key = get_key_from_hash(hash_cell(cell_x, cell_y), spatial_lookup)
        spatial_lookup[i] = SpatialEntry(i, cell_key)
        start_indices[i] = 987654321
    
    spatial_lookup.sort()

    for i in range(len(particles)):
        key = spatial_lookup[i].cell_key
        if i == 0:
            keyPrev = 987654321
        else:
            keyPrev = spatial_lookup[i - 1].cell_key
        
        if key != keyPrev:
            start_indices[key] = i


def position_to_cell_coord(particle, radius):
    cell_x = int(particle.position.x / radius)
    cell_y = int(particle.position.y / radius)
    return cell_x, cell_y


def get_key_from_hash(hash, spatial_lookup):
    return hash % len(spatial_lookup)


def hash_cell(cell_x, cell_y):
    a = cell_x * 15823
    b = cell_y * 9737333
    return a + b

