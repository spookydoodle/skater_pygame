from math import inf

import pygame
from pygame.locals import *


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, image, x = 0, y = 0):
        super().__init__()
        self.image = image
        self.rect = self.image.shape
        self.rect.x = x
        self.rect.y = y
        
    def is_under(self, other_rect):
        """
        Checks if `self` is located below `other_rect`, regardless of the distance
        """
        return self.rect.bottom > other_rect.bottom \
            and self.rect.left < other_rect.right \
            and self.rect.right > other_rect.left 

    
    def is_over(self, other_rect):
        """
        Checks if `self` is located over `other_rect`, regardless of the distance
        """
        distance = other_rect.distance_y(self.rect)
        return distance != inf and distance < 0

    def is_to_the_right(self, other_rect):
        """
        Checks if `self` is located to the right of `other_rect`, regardless of the distance

        `self` is on the right if the x_distance `other -> self` > 0
        """
        distance = other_rect.distance_x(self.rect)
        return distance != inf and distance > 0

    def is_to_the_left(self, other_rect):
        """
        Checks if `self` is located to the left of `other_rect`, regardless of the distance
        """
        distance = other_rect.distance_x(self.rect)
        return distance != inf and distance < 0