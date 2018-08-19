from unittest import TestCase

from skater.rendering.edge import Edge
from skater.rendering.point import Point

""" A set of points used by the tests
A---B
-----
--C--
-----
D---E
"""
A = Point(0, 0)
B = Point(100, 0)
C = Point(50, 50)
D = Point(0, 100)
E = Point(100, 100)

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

    def test_contains_positive(self):
        edge = Edge(D, B)
        self.assertTrue(
            edge.contains(C))

    def test_contains_negative(self):
        edge = Edge(D, B)
        self.assertFalse(
            edge.contains(A))