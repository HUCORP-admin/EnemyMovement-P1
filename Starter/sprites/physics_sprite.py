""" Module for imlpementing physics in sprite """

from abc import ABC, abstractmethod
import pygame as pg

from constants import GRAVITY
from .animated_sprite import AnimatedSprite

# pylint: disable=too-many-instance-attributes

class PhysicsSprite(ABC, AnimatedSprite):
    """ Physics sprite class for applying physics to a sprite

    :param float x - x-position of sprite
    :param float y - y-position of sprite
    :param groups - list of sprite groups that sprite belongs to
    """
    def __init__(self, x: float, y: float, *groups):
        super().__init__(groups)

        # vectors
        self.pos = pg.math.Vector2(x, y)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)

        self.max_speed = 9999
        self.max_fall_speed = 9999
        self.deceleration = 0

    @property
    def speed(self):
        """ Method to get speed from velocity vector """
        return self.vel.length()

    @property
    def speedx(self):
        """ Method to get speed in x-direction """
        return abs(self.vel.x)

    @property
    def speedy(self):
        """ Method to get speed in y-direction """
        return abs(self.vel.y)

    @speedx.setter
    def speedx(self, speed: float):
        """ Method to set speed in x-direction """
        self.vel.x = speed if self.vel.x > 0 else -speed

    @speedy.setter
    def speedy(self, speed: float):
        """ Method to set speed in y-direction """
        self.vel.y = speed if self.vel.y > 0 else -speed

    def set_speed(self, s: float):
        """ Method to set speed of velocity vector

        :param float s: magnitude of vel (new speed)
        """
        if self.speed != 0:
            if s == 0:
                self.vel = pg.math.Vector2(0, 0)
            else:
                self.vel.scale_to_length(s)

    def set_max_speed(self, ms: float):
        """ Method to set max speed of sprite

        :param float ms: maximum speed to set sprite
        """
        self.max_speed = ms

    def set_max_fall_speed(self, ms: float):
        """ Method to set max fall speed of sprite

        :param float ms: maximum fall speed of sprite
        """
        self.max_fall_speed = ms

    def set_deceleration(self, d: float):
        """ Method to set slow down value of sprite

        :param float d: deceleration value
        """
        self.deceleration = d

    @abstractmethod
    def move(self):
        """ Method to control physics movement """

    def update(self):
        """ Method to update the sprite """
        super().update()

        # apply gravity
        self.acc = pg.math.Vector2(0, GRAVITY)

        # movement
        self.move()

        # apply acceleration
        self.vel += self.acc

        # apply friction
        if abs(self.acc.x) < 0.01:
            if self.speedx < self.deceleration:
                self.speedx = 0
            else:
                self.speedx = self.speedx - self.deceleration

        # cap speed in x and y
        self.speedx = min(self.speedx, self.max_speed)
        if self.vel.y > 0:
            self.speedy = min(self.speedy, self.max_fall_speed)

        # apply velocity
        self.pos += self.vel
        self.rect.midbottom = self.pos
