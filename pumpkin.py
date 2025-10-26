import arcade
import math


from constants import SEED_DAMAGE
from constants import SEED_SPEED
from constants import PUMP_RANGE



def distance(point1,point2):

    return (   (point1.center_x - point2.center_x)**2 + (point1.center_y - point2.center_y)**2   )**0.5

class Pumpkin(arcade.Sprite):
    def __init__(self,texture,scale,location_x,location_y,range =PUMP_RANGE,damage=SEED_DAMAGE, seed_speed =SEED_SPEED):

        super().__init__(texture, scale)

        # Initializing pumpkin attributes that will be needed for methods
        self.center_x = location_x
        self.center_y = location_y
        self.range = range
        self.damage = damage
        self.seed_speed = seed_speed
        self.upgrade_level = 1
        self.targeted_enemy= None
        self.seed = False
        self.is_shooting = False
        self.current_frame = None
        self.idle_texture = arcade.load_texture("assets/images/basic_pumpkin.png")
        self.animation = [arcade.load_texture("assets/images/basic_pumpkin.png"),arcade.load_texture("assets/images/classic_2.png"),
                          arcade.load_texture("assets/images/classic_2.png"),arcade.load_texture("assets/images/classic_2.png"),
                          arcade.load_texture("assets/images/classic_2.png"),arcade.load_texture("assets/images/classic_2.png"),
                          arcade.load_texture("assets/images/classic_2.png"),arcade.load_texture("assets/images/classic_2.png"),
                          arcade.load_texture("assets/images/classic_3.png"),arcade.load_texture("assets/images/classic_3.png"),
                          arcade.load_texture("assets/images/classic_3.png"),arcade.load_texture("assets/images/classic_3.png"),
                          arcade.load_texture("assets/images/classic_3.png"),arcade.load_texture("assets/images/classic_3.png")]

    def fire_animation(self):
        self.current_frame = 0
        self.is_shooting = True
        self.texture = self.animation[self.current_frame]
    
    def target(self,enemy_list):

        #Needs the ability to check collisions between the range area (drawn object) and a sprite
        # collided_sprites = arcade.check_for_collision_with_list(self.attack_area,enemy_list)
        
        enemies_in_range = []

        for enemy in enemy_list:
            if distance(enemy,self)<self.range:
                enemies_in_range.append(enemy)
        if enemies_in_range:
            
            max_enemy =  enemies_in_range.pop()    
            for enemy in enemies_in_range:
                if enemy.center_x > max_enemy.center_x:
                    max_enemy = enemy

            self.targeted_enemy = max_enemy
        else:
            self.targeted_enemy = None
    
    def upgrade(self):
        #self.upgrade_level +=1
        print('attempting upgrade')

        if self.upgrade_level == 1:
            self.range += 10
            self.damage += 10
            self.fire_rate += 10
            print('upgrade successful')
