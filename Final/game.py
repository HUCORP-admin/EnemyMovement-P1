""" Module for creating instance of game and specifying directories """

from os import path
from base_game import BaseGame


class Game(BaseGame):
    """ Class for initializing and creating Game
    
    :param str title - title of window
    :param int width - pixel width of window
    :param int height - pixel height of window
    """
    def __init__(self, title: str, width: int, height: int):
        super().__init__(title, width, height)

        self.assets_dir = path.join(self.dir, 'assets')     # locate assets directory
        self.img_dir = path.join(self.assets_dir, 'img')	# locate img directory
        self.map_dir = path.join(self.assets_dir, 'map')    # locate map directory

        self.debug_mode = True
