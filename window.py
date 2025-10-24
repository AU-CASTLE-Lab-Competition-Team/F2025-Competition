import arcade

# from enemy import Enemy
# from pumpkin import Pumpkin
# from gate import Gate

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
        self.pumpkin_list = None
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
        self.pumpkin_list = self.map_test1.sprite_lists["pumpkins"]
        patches = {}
        for patch in self.patch_list:
            patches[patch] = [patch.center_x,patch.center_y]
        print(patches)

    def on_draw(self):
        arcade.start_render()

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
        self.pumpkin_list.draw()
        
                
def main():

    MyGameWindow(1280,720,'CASTLE HALLOWS')
    
    arcade.run()
  
main()

