import random

import numpy as np
import pygame

from .rendering.point import Point
from .rendering import shape

class Image:
    """
    A wrapper around a pygame image class. It provides a common interface for
    drawable elements.

    The code outside of this class should not use any other image-related APIs.

    `self.shape` is a pygame.rect instance for now.
    Will be replaced by another class once non-rectangular shapes are supported
    """
    def __init__(self, raw_image, shape):
        self.raw_image = raw_image
        self.shape = shape

    @classmethod
    def load(cls, path):
        """
        Loads and prepares an image from a local file
        """
        raw_image = pygame.image.load(path)
        raw_image.convert_alpha()

        pyrect = raw_image.get_rect()

        rectangle = shape.rectangle(
            Point(pyrect.left, pyrect.top),
            Point(pyrect.right, pyrect.bottom)
        )
        
        return Image(
            raw_image,
            rectangle)

    @classmethod
    def create(cls, size, color=None):
        """
        Creates a new rectangular surface
        """
        # If no color was specified, just create a random one
        color = color or cls.random_color()

        left, bottom = size

        rectangle = shape.rectangle(
            Point(0, 0),
            Point(left, bottom)
        )

        # Build the shape mask
        mask = rectangle.build_surface_mask()

        # Flip the mask - we'll use a flipped coordinate system for pixel access
        mask = mask.transpose()
        
        width = mask.shape[0]
        height = mask.shape[1]

        # Create a surface with a per-pixel alpha value
        surface = pygame.Surface(
            (width, height),
            flags=pygame.SRCALPHA)

        surface.fill(color)

        # Set pixels outside of the figure as fully transparent
        alpha = pygame.surfarray.pixels_alpha(surface)
        alpha[:] = mask * 255
        
        return Image(surface, rectangle)

    @staticmethod
    def random_color():
        # colors are integers of value <0, 255>
        lo = 0
        hi = 255

        return [
            random.randint(lo, hi)
            for _ in range(3)
        ]