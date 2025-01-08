""" Module for initializing pygame functionalities """

import sys
from os import path

import pygame as pg
from base_screen import BaseScreen


class BaseGame:
    """ Class for accessing functionalities that all games will require

    :param str title - title of window
    :param int width - pixel width of window
    :param int height - pixel height of window
    """
    def __init__(self, title: str, width: int, height: int):
        """ Initialize pygame window """
        pg.init()
        pg.display.set_caption(title)

        # screen
        self.width = width
        self.height = height

        self.screen = None
        self.surface = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()

        # current directory
        self.dir = path.dirname(__file__)

    def set_screen(self, scr: BaseScreen):
        """ Method for setting active screen on window """
        # delete existing screen
        if self.screen is not None:
            del self.screen
            self.screen = None

        self.screen = scr

        # show new screen
        if self.screen is not None:
            self.screen.show()

    def quit(self):
        """ exit the game """
        pg.quit()
        sys.exit()

    def events(self):
        """ handle events in game loop """
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.quit()
