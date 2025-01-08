""" Module for managing first level of game """

from os import path

import pygame as pg

from map import TiledMap
from game import Game
from base_screen import BaseScreen
from other_sprites import Platform
from player import Player
from enemies import MeleeEnemy, ShooterEnemy
from constants import Colors, Health, PLT_COL_TOL


class Level(BaseScreen):
    """ Class for managing level 1 of game

    :param Game game - instance of main game window
    """
    def __init__(self, game: Game):
        super().__init__(game)

        self.map = TiledMap(path.join(self.game.map_dir, 'level.tmx'))

        # extract map contents
        for obj in self.map.tmx_data.objects:
            obj_midbottom = pg.math.Vector2(obj.x + obj.width/2, obj.y + obj.height)
            if obj.name == 'player':
                self.player = Player(self.game.img_dir, obj_midbottom, self.all_sprites)
            elif obj.name == 'platform':
                Platform((obj.x, obj.y), (obj.width, obj.height), self.platforms, self.all_sprites)
            elif obj.name == 'melee':
                MeleeEnemy(self.game.img_dir, (obj.x, obj.y), self)
            elif obj.name == 'shooter':
                ShooterEnemy(self.game.img_dir, (obj.x, obj.y), self)

    def draw(self):
        self.game.surface.fill(Colors.WHITE.value)
        self.all_sprites.draw(self.game.surface)

        if self.game.debug_mode:
            for enemy in self.enemies.sprites():
                if hasattr(enemy, 'detection_box'):
                    pg.draw.rect(self.game.surface, Colors.CYAN.value, enemy.detection_box, 1)

        self.draw_player_health_bar(120, 20, self.player.health/Health.PLAYER_HEALTH.value)

        pg.display.flip()

    def update(self):
        self.all_sprites.update()
        self.check_collisions()

    def check_collisions(self):
        """ Check collisions present in level """
        # PLAYER COLLISIONS
        # collision with platforms
        hits = pg.sprite.spritecollide(self.player, self.platforms, False, pg.sprite.collide_mask)
        for hit in hits:
            self.handle_collision(self.player, hit, PLT_COL_TOL)

        # ENEMY COLLISIONS
        # collision with platforms
        hits = pg.sprite.groupcollide(
            self.enemies, self.platforms, False, False, pg.sprite.collide_mask
        )

        for sp, hit_list in hits.items():
            for hit in hit_list:
                self.handle_collision(sp, hit, PLT_COL_TOL)
