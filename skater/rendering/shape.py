from math import sqrt, ceil

import numpy as np
from PIL import Image, ImageDraw
import pygame

from .point import Point
from .edge import Edge

class Shape:
    """
    Base class for all 2-D shapes.

    Currently, `Polygon` is the only implemented type. This class is meant to be
    a common ancestor for future, non-polygon shapes (i.e. circles / splines).

    NOTE: all logic in this module will only work if the passed in indices are integers, not floats
    """
    pass

class Polygon(Shape):
    """
    A Polygon is defined by a list of vertices.
    """
    def __init__(self, vertices):
        assert(len(vertices) > 0)
        self.vertices = vertices

    def __repr__(self):
        return "{}: {}".format(
            self.__class__.__name__,
            self.vertices
        )

    def __eq__(self, other):
        return isinstance(other, Polygon) and self.vertices == other.vertices

    def clone(self):
        return Polygon(self.vertices[:])

    def shifted(self, x_shift=0, y_shift=0):
        result = self.clone()
        result.x += x_shift
        result.y += y_shift
        return result

    def centre(self):
        """
        Geometrical centre of the Polygon.

        Mean value of vertices along each axis.
        """
        mean_x = sum(vertex.x for vertex in self.vertices) / len(self.vertices)
        mean_y = sum(vertex.y for vertex in self.vertices) / len(self.vertices)
        return Point(mean_x, mean_y)

    def radius(self):
        """
        Distance between the centre and the most distant vertex
        """
        centre = self.centre()

        # Distance between each vertex and the centre, for each axis.
        distance_pairs = [
            [vertex.x - centre.x, vertex.y - centre.y]
            for vertex in self.vertices
        ]

        # Absolute distance between each vertex and the centre
        distances = [
            sqrt(pair[0] ** 2 + pair[1] ** 2)
            for pair in distance_pairs]

        return ceil(max(distances))

    def edges(self):
        # a list of self.vertives, but shifted by 1 index
        next_vertices = self.vertices[1:] + self.vertices[0:1]

        # pairs of (self.vertices[i], self.vertices[i+1])
        vertex_pairs = zip(self.vertices, next_vertices)

        return [
            Edge(vertex, next_vertex)
            for vertex, next_vertex in vertex_pairs
        ]

    def build_surface_mask(self):
        """
        Builds a 2d array describing the shape on a rectangular surface
        """
        size = 2 * self.radius()

        # Create an empty spline image
        img = Image.new('L', (size, size))

        # Draw a polygon onto the image
        vertices = [
            (v.x, v.y)
            for v in self.vertices
        ]
        ImageDraw.Draw(img).polygon(vertices, outline=1, fill=1)

        # Get a 2D array of pixel values
        mask = np.array(img)

        return mask

    def shift(self, delta):
        self.vertices = [vertex + delta for vertex in self.vertices]

    @property
    def left(self):
        return min(vertex.x for vertex in self.vertices)
    
    @property
    def right(self):
        return max(vertex.x for vertex in self.vertices)

    @property
    def top(self):
        return min(vertex.y for vertex in self.vertices)

    @property
    def bottom(self):
        return max(vertex.y for vertex in self.vertices)

    @property
    def width(self):
        return (self.right - self.left)

    @property
    def height(self):
        return (self.bottom - self.top)

    @property
    def x(self):
        return self.left

    @property 
    def y(self):
        return self.top

    @x.setter
    def x(self, value):
        value = round(value)
        shift = value - self.x
        self.shift([shift, 0])

    @y.setter
    def y(self, value):
        value = round(value)
        shift = value - self.y
        self.shift([0, shift])

    @bottom.setter
    def bottom(self, value):
        value = round(value)
        shift = value - self.bottom
        self.shift([0, shift])

    def distance_x(self, other):
        """
        Computes the shortest distance in the x direction.
        """
        # Distances between each vertex of `self` and edge of `other`
        distances_to_other = [
            edge.distance_x(vertex)
            for vertex in self.vertices
            for edge in other.edges()]

        # Analogous; -1 due to an inverted orientation
        distances_of_other = [
            -1 * edge.distance_x(vertex)
            for vertex in other.vertices
            for edge in self.edges()
        ]

        return min(distances_to_other + distances_of_other, key=abs)

    def distance_y(self, other):
        """
        Computes the shortest distance in the y direction.
        """
        distances_to_other = [
            edge.distance_y(vertex)
            for vertex in self.vertices
            for edge in other.edges()]

        distances_of_other = [
            -1 * edge.distance_y(vertex)
            for vertex in other.vertices
            for edge in self.edges()
        ]

        return min(distances_to_other + distances_of_other, key=abs)

def rectangle(top_left, bottom_right):
    bottom_left = Point(top_left.x, bottom_right.y)
    top_right = Point(bottom_right.x, top_left.y)
    return Polygon([top_left, top_right, bottom_right, bottom_left])