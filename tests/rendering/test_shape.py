from math import sqrt
from unittest import TestCase

import pygame

from skater.rendering.edge import Edge
from skater.rendering.point import Point
from skater.rendering.shape import Polygon, Rectangle

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
    def assertPixelArrayLike(self, pix_arr, data):
        pix_data = [
            [pixel for pixel in row]
            for row in pix_arr
        ]
        self.assertEqual(pix_data, data)

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

    def test_build_surface(self):
        polygon = Polygon([A, B, C])
        expected = [
            [1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        self.assertPixelArrayLike(
            pygame.PixelArray(polygon.build_surface()),
            expected)


class TestRectangle(TestCase):
    def test_creates_a_polygon(self):
        self.assertEqual(
            Rectangle(A, E),
            Polygon([A, B, E, D]))