import arcade
from enemy import Enemy
from constants import ZOMBIE_SPEED

class Zombie(Enemy):
    def __init__(self, image, scale, position_list):
        super().__init__(image, scale, position_list)

        self.speed = ZOMBIE_SPEED
        self.health = 120