import arcade
import math
#{\displaystyle d(p,q)={\sqrt {(p_{1}-q_{1})^{2}+(p_{2}-q_{2})^{2}}}.}

def distance(point1,point2):

    return (   (point1.center_x - point2.center_x)**2 + (point1.center_y - point2.center_y)**2   )**0.5

class Pumpkin(arcade.Sprite):
    def __init__(self,image,scale,location_x,location_y,range =10,damage=1, seed_speed =1):

        super().__init__(image, scale)

        # Initializing pumpkin attributes that will be needed for methods
        self.center_x = location_x
        self.center_y = location_y
        self.range = range
        self.damage = damage
        self.seed_speed = seed_speed
        self.upgrade_level = 1
        self.targeted_enemy= None
        self.seed = None

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
        

    def shoot(self):

        # This logic likely wont work here because the values wont update properly
        if not self.seed:
            self.seed = arcade.Sprite("assets/images/pumpseed.png",1,center_x = self.center_x,center_y = self.center_y)
        if self.targeted_enemy:
            while  not arcade.check_for_collision(self.seed,self.targeted_enemy):
                
                
                start_x = self.seed.center_x
                start_y = self.seed.center_y

                dest_x = self.targeted_enemy.center_x
                dest_y = self.targeted_enemy.center_y


                x_diff = dest_x - start_x
                y_diff = dest_y - start_y

                # Calculate angle to get there
                angle = math.atan2(y_diff, x_diff)

                # How far are we?
                distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

                delta_time = float(1/60)

                travel_distance = self.seed_speed * delta_time

                actual_speed = min(travel_distance, distance)

                # Calculate vector to travel
                change_x = math.cos(angle) * actual_speed
                change_y = math.sin(angle) * actual_speed

                # Update our location
                self.seed.center_x += change_x
                self.seed.center_y += change_y
                distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)
            
            print('Taking damage')
            self.seed.remove_from_sprite_lists()
            self.targeted_enemy.health -=10
            self.seed = None

                

                

            
        
            
    def place_me(self):
        pass
    
    def upgrade(self):
        self.upgrade_level +=1

        if self.upgrade_level == 1:
            self.range = 10
            self.damage = 10
            self.fire_rate = 10
