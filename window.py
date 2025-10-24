import arcade
from arcade.camera import Camera2D

from enemy import Enemy
from constants import SPRITE_SCALING_ENEMY, ENEMY_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR

from pumpkin import Pumpkin
# from gate import Gate


class MyGameWindow(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        self.set_location(400,200)

        self.cam_center_x = 0
        self.cam_center_y = 0
        self.zoom_scale = 1.0


        arcade.set_background_color(BACKGROUND_COLOR)

        self.camera = Camera2D()

        self.ground_list = None
        self.patch_list = None
        self.pumpkin_list = None
        self.path_list = None
        self.enemy_list = None
        
        self.setup()
        
    def setup(self):
        self.map_test1 = arcade.load_tilemap("assets/maps/test_map1.tmx",1)

        map_width = self.map_test1.width * self.map_test1.tile_width
        map_height = self.map_test1.height * self.map_test1.tile_height
        
        self.cam_center_x = map_width // 2
        self.cam_center_y = map_height // 2

        scale_x = self.width / map_width
        scale_y = self.height / map_height
        self.zoom_scale = min(scale_x, scale_y)

        self.ground_list = self.map_test1.sprite_lists["ground"]
        self.path_list = self.map_test1.sprite_lists["path"]
        self.patch_list = self.map_test1.sprite_lists["patches"]
        self.pumpkin_list = self.map_test1.sprite_lists["pumpkins"]
        patches = {}
        for patch in self.patch_list:
            patches[patch] = [patch.center_x,patch.center_y]
        print(patches)

        # Enemy setup
        self.enemy_list = arcade.SpriteList()

        position_list = [[20, 840],
                         [500, 840],
                         [500, 300],
                         [700, 300],
                         [700, 840],
                         [1200, 840],
                         [1200, 520],
                         [1400, 520],
                         [1400, 1000],
                         ]
        
        enemy = Enemy("assets/images/skeleton_enemy.png",
                      SPRITE_SCALING_ENEMY,
                      position_list)
        
        # Set initial location of the enemy at the first point
        enemy.center_x = position_list[0][0]
        enemy.center_y = position_list[0][1]

        self.enemy_list.append(enemy)

        # Initializing pumpkin and adding to a list of objects of type pumpkin for testing
        my_test_pumpkin = Pumpkin("assets/images/basic_pumpkin.png",1,200,200,range=1000)

        self.spawned_pumpkins = [my_test_pumpkin]
        self.path_list.append(my_test_pumpkin)

        print("Enemy initial position:", enemy.center_x, enemy.center_y)
        print("Map size:", map_width, map_height)


    def on_draw(self):
        self.clear()

        self.camera.position = (self.cam_center_x, self.cam_center_y)
        self.camera.zoom = self.zoom_scale
        self.camera.use()

        self.ground_list.draw()
        self.path_list.draw()
        self.patch_list.draw()
        self.enemy_list.draw()
        self.pumpkin_list.draw()

        #arcade.start_render()

        # self.clear()   included in documentation but untested, trying without for now
        







    def on_update(self, delta_time):
        self.enemy_list.update()

        '''Target function needs to be fixed for pumpkin'''
        # if self.spawned_pumpkins:
        #     print('checking target')
        #     my_test_pumpkin = self.spawned_pumpkins[0]
        #     isCollission = my_test_pumpkin.target(self.enemy_list)
        #     if isCollission:
        #         print('TARGETING WORKS MOTHER *UCKER')


    
            
                
def main():
    
    window = MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
  
main()

