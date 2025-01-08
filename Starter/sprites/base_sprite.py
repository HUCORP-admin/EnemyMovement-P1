""" Module for specifying base sprite properties """

import pygame as pg


class BaseSprite(pg.sprite.Sprite):
    """ Base sprite class providing common functions for pygame sprites
        
    :param groups: list of sprite groups that the sprite belongs to
    """
    def __init__(self, *groups):
        super().__init__(groups)
        self.image = None
        self.rect = None

    def set_image(self, size: tuple[int, int], color: tuple[int, int, int] | str):
        """ Method to set image and get rectangle for pygame sprite
        
        :param tuple size: size of sprite image
        :param tuple color: RGB color code or hex code to fill sprite image with
        """
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def move_to(self, pos: tuple[float, float]):
        """ Method to move sprite to specific position

        :param tuple pos: (x, y) position to move sprite to
        """
        self.rect.center = pos

    def move_by(self, x: float, y: float):
        """ Method to move sprite by a specific amount in the (x, y) directions

        :param float x: amount to move sprite by in the x direction
        :param float y: amount to move sprite by in the y direction
        """
        self.rect.x += x
        self.rect.y += y
