import arcade


class Pumpkin(arcade.Sprite()):
    def __init__(self,location_x,location_y,range =10,damage=10, fire_rate =10):
        super.__init__("assets\images\basic_pumpkin.png")
        self.x = location_x
        self.y = location_y
        self.range = range
        self.damage = damage
        self.fire_rate = fire_rate

    def target(self):
        pass

    def shoot(self):
        pass
    def place_me(self):
        pass