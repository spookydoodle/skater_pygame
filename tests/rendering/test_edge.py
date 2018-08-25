from unittest import TestCase

from skater.rendering.edge import Edge
from skater.rendering.point import Point

""" A set of points used by the tests
A---B
-F---
--C--
-----
D---E
"""
A = Point(0, 0)
B = Point(100, 0)
C = Point(50, 50)
D = Point(0, 100)
E = Point(100, 100)
F = Point(25, 25)

class TestEdge(TestCase):
    def test_get_equation_params(self):
        edge = Edge(D, B)
        self.assertEqual(
            edge.get_equation_params(),
            (-1, 100, (0, 100), (0, 100)))

    def test_get_equation_params_non_zero_x(self):
        edge = Edge(C, E)
        self.assertEqual(
            edge.get_equation_params(),
            (1, 0, (50, 100), (50, 100)))

    def test_get_equation_params_non_integer_slope(self):
        edge = Edge(
            Point(0, 0),
            Point(10, 1))
        self.assertEqual(
            edge.get_equation_params(),
            (0.1, 0, (0, 10), (0, 1)))

    def test_contains_positive(self):
        edge = Edge(D, B)
        self.assertTrue(
            edge.contains(C))

    def test_contains_negative(self):
        edge = Edge(D, B)
        self.assertFalse(
            edge.contains(A))

    def test_distance_x(self):
        edge = Edge(B, D)
        self.assertEqual(
            edge.distance_x(F),
            50)

    def test_distance_x_infinite_slope(self):
        edge = Edge(B, E)
        self.assertEqual(
            edge.distance_x(F),
            75)

    def test_distance_x_horizontal_line(self):
        edge = Edge(
            Point(3, 10),
            Point(10, 10))
        point = Point(0, 10)
        self.assertEqual(
            edge.distance_x(point),
            3)

    def test_distance_y(self):
        edge = Edge(B, D)
        self.assertEqual(
            edge.distance_y(F),
            50)

    def test_distance_y_infinite_slope(self):
        edge = Edge(D, E)
        self.assertEqual(
            edge.distance_y(F),
            75)