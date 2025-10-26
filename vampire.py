import arcade
from enemy import Enemy
from constants import VAMPIRE_SPEED

class Vampire(Enemy):
    def __init__(self, image, scale, position_list):
        super().__init__(image, scale, position_list)

        self.speed = VAMPIRE_SPEED
        self.health = 120