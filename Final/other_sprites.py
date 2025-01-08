""" Module for creating platform sprites """

import pygame as pg

from sprites.base_sprite import BaseSprite
from constants import Colors


class Platform(BaseSprite):
    """ Class for spawing platforms

    :param tuple[float, float] pos: (x, y) position of platform
    :param size[float, float] size: (width, height) of platform
    :param groups - groups sprite belongs to
    """
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], *groups):
        super().__init__(groups)
        self.image = pg.Surface(size)
        self.image.fill(Colors.BLACK.value)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mask = pg.mask.from_surface(self.image)
