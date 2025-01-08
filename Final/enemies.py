""" Module for controlling enemies """

from enum import Enum
from os import path

import pygame as pg

from sprites.character import Character
from sprites.spritesheet import SpriteSheet, Animation
from base_screen import BaseScreen
from constants import (
    Colors,
    Window,
    Spritesheet as SP,
    MeleeEnemy as ME,
    ShooterEnemy as SE
)


class Enemy(Character):
    """ Class for handling common enemy properties
    :param tuple[float, float] pos - (x, y) spawn position of enemy
    :param dict[str, float] props - properties of enemy sprite
    :param BaseScreen screen - instance of screen class for sprite groups
    :param groups - sprite groups to add sprite to
    """
    class Mode(Enum):
        """ Specify enemy current mode """
        NORMAL = 1
        TARGET = 2

    def __init__(
            self,
            pos:tuple[float, float],
            props:dict[str, float],
            screen:BaseScreen,
            det:pg.Rect,
            *groups
    ):
        super().__init__(pos, props, groups)
        self.platforms = screen.platforms
        self.target = screen.player

        self.start = self.pos.x
        self.mode = self.Mode.NORMAL
        self.detection_box = det

    def reset_path(self):
        """ Method for resetting enemy path """
        self.vel.x = 0
        self.start = self.pos.x
        self.direction = 1 if self.direction == -1 else -1

    def detect_target(self):
        """ Method for handling detection box """
        self.detection_box.centerx = self.pos.x
        self.detection_box.bottom = self.rect.bottom

        if pg.Rect.colliderect(self.detection_box, self.target.rect):
            self.mode = self.Mode.TARGET
        else:
            self.mode = self.Mode.NORMAL

    def move(self):
        """ Method for moving enemy """
        if self.mode == self.Mode.NORMAL:
            travelled = abs(self.pos.x - self.start)

            if travelled < self.props.get('md'):
                self.acc.x = self.direction*self.props.get('acc')
            else:
                self.reset_path()

    def update(self):
        """ Method for updating enemy """
        super().update()
        self.detect_target()

        # restrict out-of-screen movement
        if (self.direction == -1 and self.rect.left < 0) or \
            (self.direction == 1 and self.rect.right > Window.WIDTH.value):
            self.reset_path()

        # restrict off-platform movement
        platform = pg.sprite.spritecollideany(self, self.platforms)
        if platform is not None:
            if (self.direction == 1 and self.rect.right > platform.rect.right) or \
                (self.direction == -1 and self.rect.left < platform.rect.left):
                self.reset_path()


class MeleeEnemy(Enemy):
    """ Class for handling melee enemy
    :param str img - filename for spritesheet
    :param tuple[float, float] pos - (x, y) spawn position of enemy
    :param screen - screen enemy is spawned on
    :param groups - sprite groups enemy belongs to
    """
    def __init__(self, img:str, pos:tuple[float, float], screen:BaseScreen):
        props = {
            'ms': ME.MAX_SPEED.value,
            'mf': ME.MAX_FALL_SPEED.value,
            'dec': ME.DECELERATION.value,
            'md': ME.MAX_DIST.value,
            'acc': ME.ACC.value
        }

        super().__init__(
            pos,
            props,
            screen,
            pg.Rect(*ME.DETECTION_BOX.value),
            screen.all_sprites, screen.enemies
        )

        self.load(img)
        self.screen = screen
        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def load(self, img:str):
        """ Method for extracting frames from spritesheet
        :param str img - path of spritesheet
        """
        sp_path = path.join(img, SP.MELEE_ENEMY_SPRITESHEET.value)
        spritesheet = SpriteSheet(sp_path, Colors.DARK_BLUE.value)

        frames = {
            'walk': [(8, 94, 46, 74), (65, 94, 50, 72), (127, 93, 37, 73), (172, 93, 39, 75),
                     (219, 94, 42, 74), (274, 93, 41, 75), (320, 93, 49, 75)],
            'attack': [(6, 176, 46, 80), (56, 172, 52, 84), (138, 260, 63, 75), (207, 262, 39, 73)],
            'death': [(85, 331, 53, 47), (153, 354, 72, 32), (234, 367, 74, 26),
                      (313, 374, 80, 19)]
        }

        frame_settings = {
            'walk': { 'duration': 0.15, 'mode': Animation.PlayMode.LOOP },
            'attack': { 'duration': 0.25, 'mode': Animation.PlayMode.NORMAL },
            'death': { 'duration': 0.2, 'mode': Animation.PlayMode.NORMAL }
        }

        for key, val in frames.items():
            anim = spritesheet.get_anim(val, frame_settings[key])
            self.store_animation(key, anim)

    def animate(self):
        """ Method for controlling active animations """
        if self.active_name == "attack":
            if self.is_animation_finished():
                self.set_active_animation('walk')

        self.update_image(self.direction == -1)
        self.mask = pg.mask.from_surface(self.image)

    def move(self):
        """ Method for melee enemy movement """
        super().move()
        if self.mode == self.Mode.TARGET:
            self.direction = 1 if self.target.rect.centerx > self.rect.centerx else -1
            self.acc.x = self.direction*ME.ACC.value

    def update(self):
        """ Method for updating enemy sprite """
        super().update()
        self.animate()


class ShooterEnemy(Enemy):
    """ Class for handling shooter enemy
    :param str img - filename for spritesheet
    :param tuple[float, float] pos - (x, y) spawn position of enemy
    :param screen - screen enemy is spawned on
    """
    def __init__(self, img:str, pos: tuple[float, float], screen: BaseScreen):
        props = {
            'ms': SE.MAX_SPEED.value, 
            'mf': SE.MAX_FALL_SPEED.value, 
            'dec': SE.DECELERATION.value,
            'md': SE.MAX_DIST.value,
            'acc': SE.ACC.value
        }
        super().__init__(
            pos,
            props,
            screen,
            pg.Rect(*SE.DETECTION_BOX.value),
            screen.all_sprites, screen.enemies
        )
        self.screen = screen

        self.load(img)
        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def load(self, img:str):
        """ Method for extracting frames from spritesheet """
        sp_path = path.join(img, SP.SHOOTER_ENEMY_SPRITESHEET.value)
        spritesheet = SpriteSheet(sp_path, Colors.MAGENTA.value)

        frames = {
            'walk': [(1, 89, 44, 70), (51, 87, 45, 72), (102, 85, 43, 74), (148, 85, 40, 74),
                     (195, 86, 37, 73), (236, 88, 37, 71), (279, 89, 46, 68), (329, 90, 45, 69),
                     (378, 87, 43, 72), (424, 87, 40, 72), (469, 88, 37, 71), (513, 89, 36, 70)],
            'shoot': [(2, 170, 36, 70), (41, 167, 49, 73), (96, 170, 56, 70), (159, 167, 84, 73),
                      (246, 167, 49, 73), (301, 170, 56, 70), (364, 170, 36, 70)],
            'attack': [(1, 318, 37, 72), (41, 320, 50, 70), (97, 325, 66, 65), (165, 320, 50, 70),
                      (223, 318, 37, 72)],
            'death': [(399, 482, 72, 51), (484, 494, 67, 41), (562, 531, 72, 28)]
        }

        frame_settings = {
            'walk': { 'duration': 0.15, 'mode': Animation.PlayMode.LOOP },
            'shoot': { 'duration': 0.15, 'mode': Animation.PlayMode.NORMAL },
            'attack': { 'duration': 0.3, 'mode': Animation.PlayMode.NORMAL },
            'death': { 'duration': 0.2, 'mode': Animation.PlayMode.NORMAL }
        }

        for key, val in frames.items():
            anim = spritesheet.get_anim(val, frame_settings[key])
            self.store_animation(key, anim)

        self.set_active_animation("walk")

    def animate(self):
        """ Method for controlling active animations """
        if self.active_name == "attack":
            if self.is_animation_finished():
                self.set_active_animation("walk")

        if self.active_name == "shoot":
            if self.is_animation_finished():
                self.set_active_animation("walk")

        self.update_image(self.direction == -1)
        self.mask = pg.mask.from_surface(self.image)

    def move(self):
        """ Method for controlling shooter motion """
        super().move()
        if self.mode == self.Mode.TARGET:
            pass

    def update(self):
        """ Method for updating shooter enemy sprite """
        super().update()
        self.animate()
