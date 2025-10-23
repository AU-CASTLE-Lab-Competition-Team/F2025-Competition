import arcade

from enemy import Enemy
# from pumpkin import Pumpkin
# from gate import Gate

# Constants for enemy
SPRITE_SCALING_ENEMY = 0.5
ENEMY_SPEED = 3.0


class MyGameWindow(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        self.set_location(400,200)

        self.center_x = 0
        self.center_y = 0
        self.zoom_scale = 0

        arcade.set_background_color(arcade.color.GRAY_BLUE)

        self.camera = arcade.Camera(self.width,self.height)

        self.ground_list = None
        self.patch_list = None
        self.path_list = None
        self.enemy_list = None
        
        self.setup()
        
    def setup(self):
        self.map_test1 = arcade.load_tilemap("assets/maps/test_map1.tmx",1)

        map_width = self.map_test1.width * self.map_test1.tile_width
        map_height = self.map_test1.height * self.map_test1.tile_height
        
        self.center_x = map_width // 2
        self.center_y = map_height // 2

        scale_x = self.width / map_width
        scale_y = self.height / map_height
        self.zoom_scale = min(scale_x, scale_y)

        self.ground_list = self.map_test1.sprite_lists["ground"]
        self.path_list = self.map_test1.sprite_lists["path"]
        self.patch_list = self.map_test1.sprite_lists["patches"]

        # Enemy setup
        self.enemy_list = arcade.SpriteList()

        position_list = [[50, 50],
                         [700, 50],
                         [700, 500],
                         [50, 500]]
        
        enemy = Enemy(":assets:images/animated_characters/skeleton_enemy.png",
                      SPRITE_SCALING_ENEMY,
                      position_list)
        
        # Set initial location of the enemy at the first point
        enemy.center_x = position_list[0][0]
        enemy.center_y = position_list[0][1]

        self.enemy_list.append(enemy)


    def on_draw(self):
        arcade.start_render()

        # self.clear()   included in documentation but untested, trying without for now
        self.enemy_list.draw()

        half_width = self.width / (2 * self.zoom_scale)
        half_height = self.height / (2 * self.zoom_scale)

        left = self.center_x - half_width
        right = self.center_x + half_width
        bottom = self.center_y - half_height
        top = self.center_y  + half_height

        arcade.set_viewport(left,right,bottom,top)

        self.ground_list.draw()
        self.path_list.draw()
        self.patch_list.draw()
        
    def on_update(self, delta_time):
        self.enemy_list.update()
                
def main():

    MyGameWindow(1920,1080,'CASTLE HALLOWS')
    MyGameWindow.setup() #added from documentation
    arcade.run()
  
main()

