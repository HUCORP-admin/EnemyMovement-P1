""" Module for launching game and setting screen """

from game import Game
from constants import Window
from level import Level

class Launcher(Game):
    """ Class for launching game and starting level """
    def __init__(self):
        super().__init__(Window.TITLE.value, Window.WIDTH.value, Window.HEIGHT.value)
        self.fps = Window.FPS.value   # set game FPS

    def start(self):
        """ Method for starting game to level screen """
        lvl = Level(self)
        self.set_screen(lvl)


if __name__ == '__main__':
    launcher = Launcher()
    launcher.start()
