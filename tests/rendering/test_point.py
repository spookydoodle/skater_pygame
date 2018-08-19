from unittest import TestCase

from skater.rendering.point import Point

class TestPoint(TestCase):
    def test_within_positive(self):
        point = Point(10, 10)
        self.assertTrue(
            point.within((0, 20), (0, 20)))

    def test_within_negative(self):
        point = Point(10, 10)
        self.assertFalse(
            point.within((0, 20), (0, 5)))