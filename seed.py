import arcade
import math

class Seed(arcade.Sprite):
    def __init__(self,image,scale,pumpkin):
        super().__init__(image, scale)
        self.center_x = pumpkin.center_x 
        self.center_y = pumpkin.center_y
        pumpkin.seed = True
        self.pumpkin = pumpkin
        self.target = self.pumpkin.targeted_enemy



    def update(self, delta_time: float = 1/60):
        
        
        if self.target:
            start_x = self.center_x
            start_y = self.center_y
            dest_x = self.target.center_x
            dest_y = self.target.center_y

            # X and Y difference between start and destination
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y

            # Calculate angle to get there
            angle = math.atan2(y_diff, x_diff)

            # How far are we?
            distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

            travel_distance = self.pumpkin.seed_speed * delta_time

            actual_speed = min(travel_distance, distance)

            # Calculate vector to travel
            change_x = math.cos(angle) * actual_speed
            change_y = math.sin(angle) * actual_speed

            # Update our location
            self.center_x += change_x
            self.center_y += change_y

            if arcade.check_for_collision(self,self.target):
                self.target.health -= self.pumpkin.damage
                self.pumpkin.seed = False
                self.remove_from_sprite_lists()

                
