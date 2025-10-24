import arcade


class Pumpkin(arcade.Sprite()):
    def __init__(self,location_x,location_y,range =10,damage=10, fire_rate =10):
        super.__init__("assets\images\basic_pumpkin.png")



        # Initializing pumpkin attributes that will be needed for methods
        self.x = location_x
        self.y = location_y
        self.range = range
        self.damage = damage
        self.fire_rate = fire_rate
        self.attack_area = self.calc_attack_area()
        self.upgrade_level = 1

    def calc_attack_area(self):


        attack_area = arcade.draw_circle_filled(self.x,self.y,self.range,(0,0,0,0))

        return attack_area

    def target(self,enemy_list):
        arcade.check_for_collision_with_list(self.attack_area,enemy_list)
        
    def shoot(self):
        pass


    def place_me(self):
        pass
    
    def upgrade(self):
        self.upgrade_level +=1

        if self.upgrade_level == 1:
            self.range = 10
            self.damage = 10
            self.fire_rate = 10
