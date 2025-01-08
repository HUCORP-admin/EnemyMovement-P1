""" Module for storing constants """

from enum import Enum

TILESIZE = 32
PLT_COL_TOL = 32
GRAVITY = 0.98
BULLET_ACC = 0.10
BULLET_DMG = 20

# window
class Window(Enum):
    """ Window constants """
    TITLE = 'Enemy Demo'
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60


# spritesheets
class Spritesheet(Enum):
    """ Spritesheet constants """
    PLAYER_SPRITESHEET = 'player_spritesheet.png'
    MELEE_ENEMY_SPRITESHEET = 'melee_enemy_spritesheet.png'
    SHOOTER_ENEMY_SPRITESHEET = 'shooter_enemy_spritesheet.png'

class Health(Enum):
    """ Image constants """
    PLAYER_BAR = 'player_health_bar.png'
    PLAYER_BAR_WIDTH = 200
    PLAYER_BAR_HEIGHT = 50
    PLAYER_HEALTH = 100


# player
class Player(Enum):
    """ Player constants """
    SCALE = 1.2
    MAX_SPEED = 4
    MAX_FALL_SPEED = 3
    IMPULSE = 5
    DECELERATION = 2
    ACC = 0.5
    JUMP = -15
    MELEE = 5

# enemy
class MeleeEnemy(Enum):
    """ Melee enemy constants """
    MAX_SPEED = 2
    MAX_FALL_SPEED = 4
    DECELERATION = 2
    ACC = 0.05
    MAX_DIST = 250
    DETECTION_BOX = (0, 0, 400, 110)
    MELEE_RANGE = 40
    DAMAGE = 10


# shooter enemy
class ShooterEnemy(Enum):
    """ Shooter enemy constants """
    MAX_SPEED = 1.5
    MAX_FALL_SPEED = 10
    DECELERATION = 4
    ACC = 0.025
    MAX_DIST = 200
    DETECTION_BOX = (0, 0, 600, 100)
    MELEE_RANGE = 80
    DAMAGE = 15


# colors
class Colors(Enum):
    """ Color enemy constants """
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    LIGHT_GREEN = (34, 177, 76)
    CYAN = (0, 255, 255)
    DARK_BLUE = (0, 64, 128)
    MAGENTA = (153, 41, 189)
    RED = (255, 0, 0)
    LIGHT_ORANGE = (248, 120, 0)
