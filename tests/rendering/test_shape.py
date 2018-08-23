from math import sqrt
from unittest import TestCase

import numpy as np
import pygame

from skater.rendering.edge import Edge
from skater.rendering.point import Point
from skater.rendering.shape import Polygon, rectangle

""" A set of points used by the tests
A---B
-----
--C--
-----
D---E
"""
A = Point(0, 0)
B = Point(4, 0)
C = Point(2, 2)
D = Point(0, 4)
E = Point(4, 4)

class TestPolygon(TestCase):
    def test_centre(self):
        polygon = Polygon([A, B, E, D])
        self.assertEqual(
            polygon.centre(),
            C)

    def test_radius(self):
        polygon = Polygon([A, B, E, D])
        self.assertEqual(
            polygon.radius(),
            2 * sqrt(2))

    def test_edges(self):
        polygon = Polygon([A, B, C])
        expected = [
            Edge(A, B),
            Edge(B, C),
            Edge(C, A)
        ]
        self.assertEqual(
            polygon.edges(),
            expected)

    def test_build_surface_mask(self):
        polygon = Polygon([A, B, C])
        expected = np.array([
            [1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])
        self.assertTrue(
            np.array_equal(
                polygon.build_surface_mask(),
                expected))

    def test_distance_x_positive(self):
        first = Polygon([A, D])
        other = Polygon([B, C, E])
        self.assertEqual(
            first.distance_x(other),
            2)

    def test_distance_x_negative(self):
        first = Polygon([B, E])
        other = Polygon([A, C, D])
        self.assertEqual(
            first.distance_x(other),
            -2)

    def test_distance_y_positive(self):
        first = Polygon([A, B])
        other = Polygon([C, E, D])
        self.assertEqual(
            first.distance_y(other),
            2)

class TestRectangle(TestCase):
    def test_creates_a_polygon(self):
        self.assertEqual(
            rectangle(A, E),
            Polygon([A, B, E, D]))