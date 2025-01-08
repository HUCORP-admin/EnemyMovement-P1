""" Module for controlling spritesheets """

from enum import Enum
import pygame as pg


class Animation:
    """
    Class for configuring Animation
    
    :param frames
    :param frame_duration
    :param mode
    """
    class PlayMode(Enum):
        """ Enum for different animation play modes """
        NORMAL = 1
        LOOP = 2

    def __init__(self, frames: list[pg.Surface], frame_duration: float, mode: PlayMode):
        self.frames = frames
        self.frame_duration = frame_duration
        self.animation_duration = len(self.frames)*self.frame_duration
        self.mode = mode

    def get_frame(self, state_time: float):
        """ Method to get frame from list
        :param float state_time - time elapsed to get index of frame
        """
        frame_number = self.get_frame_index(state_time)
        return self.frames[frame_number]

    def get_frame_index(self, state_time: float):
        """ Method to get index of frame in list
        :param float state_time - time elapsed to get index of frame
        """
        if len(self.frames) == 1:
            return 0

        frame_number = int(state_time/self.frame_duration)

        if self.mode == self.PlayMode.NORMAL:
            frame_number = min(len(self.frames) - 1, frame_number)
        elif self.mode == self.PlayMode.LOOP:
            frame_number = frame_number % len(self.frames)

        return frame_number

    def is_animation_finished(self, state_time: float):
        """ Method to check if on last frame
        :param float state_time - time elapsed to get index of frame
        """
        frame_number = int(state_time/self.frame_duration)
        return len(self.frames) - 1 < frame_number


class SpriteSheet:
    """ Class for managing spritesheeets
    
    :param str filename - spritesheet file
    :param tuple[int, int, int] - RGB color of background to filter
    """
    def __init__(self, filename: str, bg: tuple[int, int, int] = None):
        self.spritesheet = pg.image.load(filename).convert()
        self.bg = bg

    def get_image(
            self, frame: tuple[float, float, float, float], scale:float = None, flip:bool = False
    ):
        """ Method for extracting image from spritesheet
        
        :param tuple[float, float, float, float] frame - (x, y, w, h) of frame
        :param float scale - value to scale up/down image
        :param boolean flip - toggle flipping of image
        """
        image = self.spritesheet.subsurface(pg.Rect(frame))

        if scale is not None:
            image = pg.transform.scale(image, (frame[2]*scale, frame[3]*scale))

        if flip:
            image = pg.transform.flip(image, True, False)

        if self.bg is not None:
            image.set_colorkey(self.bg)

        return image

    def get_anim(
            self, coords: tuple[float, float, float, float], settings: {'duration', 'mode'},
            scale: float = None, flip: bool = False
    ):
        """ Method for extracting images & create animation

        :param tuple[float, float, float, float] coords - frame (x, y, w, h)
        :param {'duration', 'mode'} settings - duration and playmode for animation
        :param float scale - scale factor to apply to each frame
        :param bool flip - flip the image if needed
        """
        frames = [self.get_image(frame, scale, flip) for frame in coords]
        return Animation(frames, settings['duration'], settings['mode'])
