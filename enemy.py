import arcade
import math

from constants import ENEMY_SPEED

class Enemy(arcade.Sprite):

    def __init__(self, image, scale, position_list,health=100, ):
        super().__init__(image, scale)
        self.position_list = position_list
        self.cur_position = 0
        self.speed = ENEMY_SPEED
        self.health =health
    
    def update(self, delta_time: float = 1/60):
        # Starting position
        start_x = self.center_x
        start_y = self.center_y

        # Where the enemy is going

        dest_x = self.position_list[self.cur_position][0]
        dest_y = self.position_list[self.cur_position][1]

        # X and Y difference between start and destination
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        travel_distance = self.speed * delta_time

        actual_speed = min(travel_distance, distance)

        # Calculate vector to travel
        change_x = math.cos(angle) * actual_speed
        change_y = math.sin(angle) * actual_speed

        # Update our location
        self.center_x += change_x
        self.center_y += change_y

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # If we are there, head to the next point.
        if distance <= travel_distance:
            if self.cur_position != 8: #Number 8 based on the number of points in the position list, cur_position is an index
                self.cur_position += 1
            
            '''
            # Reached the end of the list, start over.
            if self.cur_position >= len(self.position_list):
                self.cur_position = 0
            '''
                

        