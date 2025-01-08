""" Module for animated sprite base class"""

import pygame as pg

from constants import Window
from .base_sprite import BaseSprite
from .spritesheet import Animation


class AnimatedSprite(BaseSprite):
    """ Class for controlling spritesheet animations in sprite
    
    :param groups - list of sprite groups that the sprite belongs to
    """
    def __init__(self, *groups):
        super().__init__(groups)

        # control
        self.elapsed_time = 0
        self.active_anim = None
        self.active_name = ""
        self.animation_storage = {}

    def store_animation(self, name: str, anim: Animation):
        """ Method for storing animation object as a name in dictionary for quick access

        :param str name: name to be stored as key in animation dictionary
        :param Animation anim: Animation object to be stored in dictionary
        """
        self.animation_storage[name] = anim

        # if no animation playing, start this one
        if self.active_name == "":
            self.set_active_animation(name)

    def set_active_animation(self, name: str):
        """ Method for setting active animation using name in dictionary

        :param str name: key in dictionary to get value from
        """
        if name not in self.animation_storage:
            print(f'No animation: {name}')
            return

        # check if this animation is already running
        if name == self.active_name:
            return

        self.active_name = name
        self.active_anim = self.animation_storage[name]
        self.elapsed_time = 0

    def is_animation_finished(self):
        """ Method for checking if active animation is finished

        """
        return self.active_anim.is_animation_finished(self.elapsed_time)

    def update_image(self, flip=False):
        """ Method for updating rect and image after applying animation
        :param flip - flips image if condition meant
        """
        rect = self.rect
        self.image = self.active_anim.get_frame(self.elapsed_time)

        # flip image if necessary
        if flip:
            self.image = pg.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.midbottom = rect.midbottom

    def update(self):
        """ Method for updating sprite and increasing elapsed time for anim """
        super().update()
        # update with time since last frame
        self.elapsed_time += 1/Window.FPS.value
