""" Module for controlling player functionalities """

from os import path

import pygame as pg

from sprites.character import Character
from sprites.spritesheet import SpriteSheet, Animation
from constants import Colors, Spritesheet as SP, Player as Consts


class Player(Character):
    """ Class for managing player
    
    :param str img_dir - image directory for player spritesheet
    :param tuple[float, float] pos - (x, y) position of player
    :param groups - groups sprite belongs to
    """
    def __init__(self, img_dir: str, pos: tuple[float, float], *groups):
        props = {
            'ms': Consts.MAX_SPEED.value, 
            'mf': Consts.MAX_FALL_SPEED.value, 
            'dec': Consts.DECELERATION.value,
        }

        super().__init__(pos, props, groups)
        self.jumping = False

        self.load(img_dir)

        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def load(self, img:str):
        """ Method for loading frames from spriteshet """
        sp_path = path.join(img, SP.PLAYER_SPRITESHEET.value)
        spritesheet = SpriteSheet(sp_path, Colors.LIGHT_GREEN.value)

        frames = {
            'stand': [(28, 247, 34, 63), (73, 248, 34, 62), (115, 248, 35, 61)],
            'run': [(22, 346, 62, 55), (88, 348, 65, 49), (160, 345, 65, 54),
                    (238, 344, 53, 56), (296, 338, 60, 57), (365, 342, 63, 51),
                    (433, 343, 65, 52), (503, 343, 58, 55)],
            'jump': [(609, 343, 43, 51), (664, 337, 48, 64), (720, 338, 48, 64)],
            'fall': [(773, 344, 60, 50), (839, 323, 44, 80), (897, 326, 46, 77)],
            'land': [(960, 336, 47, 69), (1023, 362, 47, 43), (1081, 352, 42, 52)],
            'attack1': [(34, 724, 53, 51), (93, 722, 78, 51), (176, 723, 75, 51),
                        (259, 723, 73, 51), (336, 718, 52, 56)],
            'attack2': [(616, 711, 53, 60), (677, 715, 50, 56), (734, 718, 78, 53),
                        (821, 718, 77, 53), (906, 717, 59, 54)],
            'attack3': [(24, 845, 51, 55), (86, 848, 55, 53), (150, 847, 82, 54),
                        (240, 847, 80, 54), (327, 846, 67, 55), (403, 848, 46, 53)],
            'throw': [(20, 1004, 46, 54), (81, 997, 53, 61), (149, 1004, 82, 54),
                      (239, 1004, 72, 54), (326, 1003, 67, 55)],
            'death': [(216, 598, 54, 60), (281, 610, 67, 47), (367, 636, 71, 19)],
            'damage1': [(37, 595, 46, 60)],
            'damage2': [(95, 601, 44, 54)]
        }

        frame_settings = {
            'stand': { 'duration': 0.2, 'mode': Animation.PlayMode.LOOP },
            'run': { 'duration': 0.1, 'mode': Animation.PlayMode.LOOP },
            'jump': { 'duration': 0.05, 'mode': Animation.PlayMode.NORMAL },
            'fall': { 'duration': 0.1, 'mode': Animation.PlayMode.NORMAL },
            'land': { 'duration': 0.1, 'mode': Animation.PlayMode.NORMAL },
            'attack1': { 'duration': 0.05, 'mode': Animation.PlayMode.NORMAL },
            'attack2': { 'duration': 0.05, 'mode': Animation.PlayMode.NORMAL },
            'attack3': { 'duration': 0.1, 'mode': Animation.PlayMode.NORMAL },
            'throw': { 'duration': 0.1, 'mode': Animation.PlayMode.NORMAL },
            'death': { 'duration': 0.15, 'mode': Animation.PlayMode.NORMAL },
            'damage1': { 'duration': 0.25, 'mode': Animation.PlayMode.NORMAL },
            'damage2': { 'duration': 0.25, 'mode': Animation.PlayMode.NORMAL },
            'damage3': { 'duration': 0.25, 'mode': Animation.PlayMode.NORMAL }
        }

        for key, val in frames.items():
            anim = spritesheet.get_anim(val, frame_settings[key], scale=Consts.SCALE.value)
            self.store_animation(key, anim)

    def attack(self):
        """ Method for attacking """
        if self.attack_count == 0:
            self.set_active_animation('attack1')
        elif self.attack_count == 1:
            self.set_active_animation('attack2')
        elif self.attack_count == 2:
            self.set_active_animation('attack3')

    def run(self, direction: int = 1):
        """ Method for controlling running """
        if self.direction != direction:
            self.vel.x = 0
            self.direction = direction

        if abs(self.vel.x) == 0:
            # player not moving - apply impulse
            self.acc.x = direction*Consts.IMPULSE.value
        else:
            self.acc.x = direction*Consts.ACC.value

    def move(self):
        """ Method for checking key presses """
        if self.health > 0:
            keys = pg.key.get_pressed()

            if self.active_name != 'land' and 'damage' not in self.active_name:
                if keys[pg.K_j]:
                    self.attack()
                elif keys[pg.K_d]:
                    self.run()
                elif keys[pg.K_a]:
                    self.run(-1)

            if keys[pg.K_w]:
                if self.ground_count > 0 and not self.jumping and self.attack_count == 0:
                    self.vel.y = Consts.JUMP.value
                    self.ground_count = 0
                    self.jumping = True
            else:
                self.jumping = self.active_name not in ('stand', 'run')

    def animate_jumps(self):
        """ Method for changing jump/fall animations """
        if self.active_name == "jump":
            if self.vel.y > 0:
                self.set_active_animation("fall")

        if self.active_name == "fall":
            if self.ground_count > 0:
                self.set_active_animation("land")

        if self.active_name == "land":
            if self.is_animation_finished():
                if abs(self.vel.x) > 0:
                    self.set_active_animation("run")
                else:
                    self.set_active_animation("stand")
            else:
                self.vel.x = 0

    def animate_attacks(self):
        """ Method for changing attack animations """
        if self.active_name == 'attack1':
            if self.is_animation_finished():
                if self.attack_count > 1:
                    self.set_active_animation('attack2')
                else:
                    self.attack_count = 0
                    self.set_active_animation("stand")

        if self.active_name == 'attack2':
            if self.is_animation_finished():
                if self.attack_count > 2:
                    self.set_active_animation('attack3')
                else:
                    self.attack_count = 0
                    self.set_active_animation("stand")

        if self.active_name == 'attack3':
            if self.is_animation_finished():
                self.attack_count = 0
                self.set_active_animation("stand")

    def animate_damage(self):
        """ Method for controlling damage animations """
        if self.active_name == "damage1":
            if self.is_animation_finished():
                self.set_active_animation("stand")
        if self.active_name == "damage2":
            if self.is_animation_finished():
                self.set_active_animation("stand")

    def animate(self):
        """ Method for controlling animations """
        if self.active_name == "run":
            if self.vel.x == 0:
                self.set_active_animation("stand")

            if self.vel.y < 0:
                self.set_active_animation("jump")

        if self.active_name == "stand":
            if abs(self.vel.x) > 0:
                self.set_active_animation("run")

            if self.vel.y < 0:
                self.set_active_animation("jump")

        self.animate_jumps()
        self.animate_attacks()
        self.animate_damage()

        self.update_image(self.direction == -1)
        self.mask = pg.mask.from_surface(self.image)

    def damage(self, dmg:int):
        """ Method for controlling player damage """
        self.health -= dmg
        if self.active_name == "damage1":
            self.set_active_animation("damage2")
        elif self.active_name == "damage2":
            self.set_active_animation("damage1")
        else:
            self.set_active_animation("damage1")

    def update(self):
        """ Method for updating player """
        super().update()
        self.animate()

        if self.health <= 0:
            self.set_active_animation("death")
