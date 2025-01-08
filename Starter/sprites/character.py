""" Module for controlling character sprites """

from constants import Window
from .physics_sprite import PhysicsSprite


class Character(PhysicsSprite):
    """ Character class for shared properties of player and enemy sprites

    :param tuple[float, float] pos - (x, y) position of character position
    :param props - properties for max speed, max fall speed, deceleration
    :param groups - groups character belongs to
    """
    def __init__(self, pos: tuple[float, float], props: dict[str, int], *groups):
        super().__init__(pos[0], pos[1], groups)

        self.health = 100
        self.ground_count = 0
        self.shoot_count = 0
        self.attack_count = 0
        self.direction = 1
        self.props = props

        self.set_max_speed(props.get('ms'))
        self.set_max_fall_speed(props.get('mf'))
        self.set_deceleration(props.get('dec'))

    def update(self):
        """ Update method """
        super().update()

        # constraint character motion within screen
        if self.rect.left < 0:
            self.pos.x = 0 + (self.rect.right - self.rect.left)/2

        if self.rect.right > Window.WIDTH.value:
            self.pos.x = Window.WIDTH.value - (self.rect.right - self.rect.left)/2
