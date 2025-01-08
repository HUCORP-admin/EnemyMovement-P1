""" Module for calling game functionalities for screen """

from abc import ABC, abstractmethod
from os import path

import pygame as pg

from sprites.character import Character
from sprites.base_sprite import BaseSprite
from constants import Health, Colors


class BaseScreen(ABC):
    """ Class for creating and managing scren

    :param BaseGame game - instance of base game class
    """
    def __init__(self, game):
        self.game = game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

    def show(self):
        """ Method for controlling game loop """
        while True:
            self.game.clock.tick(self.game.fps)
            self.game.events()
            self.update()
            self.draw()

    @abstractmethod
    def draw(self):
        """ Method for drawing items to the screen """

    @abstractmethod
    def update(self):
        """ Method for updating content on screen """

    def draw_player_health_bar(self, x: float, y: float, pct: float):
        """ Method for drawing player health bar
        :param float x - x coordinate of health bar
        :param float y - y coordinate of health bar
        :param float pct - remaining health factor apply to health bar fill
        """
        # prepare outline
        image = pg.image.load(path.join(self.game.img_dir, Health.PLAYER_BAR.value))
        image = pg.transform.scale(
            image, (Health.PLAYER_BAR_WIDTH.value, Health.PLAYER_BAR_HEIGHT.value)
        )
        image.set_colorkey(Colors.BLACK.value)

        # position
        x = x - Health.PLAYER_BAR_WIDTH.value/2

        fill = pct*(Health.PLAYER_BAR_WIDTH.value - 42)
        fill_rect = pg.Rect(x + 42, y + 35, fill, Health.PLAYER_BAR_HEIGHT.value/4)

        if pct > 0.3:
            color = Colors.LIGHT_ORANGE.value
        else:
            color = Colors.RED.value

        self.game.surface.blit(image, (x, y))
        pg.draw.rect(self.game.surface, color, fill_rect)

    def handle_collision(self, character: Character, hit: BaseSprite, tolerance: int):
        """ Method for controliing collisions between characters and obstacles
        
        :param Character character - character sprite that collides with obstacle
        :param BaseSprite hit - the sprite character hits
        :param int tolerance - used to check if character passes into hit sprite
        """
        # character's bottom and obstacle top
        if abs(hit.rect.top - character.rect.bottom) < hit.rect.height/2:
            character.vel.y = 0
            if isinstance(hit, Character):
                character.vel.x = 0
                if character.pos.x < hit.pos.x:
                    character.pos.x = hit.rect.left - character.rect.width/2 - 1
                else:
                    character.pos.x = hit.rect.right + character.rect.width/2 + 1
            else:
                character.pos.y = hit.rect.top + 1
                character.ground_count = 1

        # character's top and obstacle bottom
        if abs(hit.rect.bottom - character.rect.top) < hit.rect.height/2:
            character.vel.y = 0
            char_height = character.rect.bottom - character.rect.top
            character.pos.y = (hit.rect.bottom - 1) + char_height

        # character's left and obstacle right
        if abs(hit.rect.right - character.rect.left) < tolerance:
            character.acc.x = 0
            character.vel.x = 0
            character.pos.x = hit.rect.right + character.rect.width/2 + 1

        # character's right and obstacle left
        if abs(hit.rect.left - character.rect.right) < tolerance:
            character.acc.x = 0
            character.vel.x = 0
            character.pos.x = hit.rect.left - character.rect.width/2 - 1
