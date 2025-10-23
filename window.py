import arcade

class MyGameWindow(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        self.set_location(400,200)
        #self.pathSprite = arcade.Sprite("assets\images\deadgrass_tile.png",center_x=100,center_y=100)
        
        arcade.set_background_color(arcade.color.GREEN)
        
        self.ground_list = None
        self.patch_list = None
        self.path_list = None
        self.enemy_list = None
        
        self.setup()
        
    def setup(self):
        map_test1 = arcade.load_tilemap("assets/maps/test_map1.tmx",1)
        self.ground_list = map_test1.sprite_lists["grass_tile"]
        self.path_list = arcade.generate_sprites(map_test1,"pathtile_lr",1)
        self.path_list += arcade.generate_sprites(map_test1,"pathtile_ud",1)
        self.patch_list = arcade.generate_sprites(map_test1,"pumpatchv1",1)

    def on_draw(self):
        arcade.start_render()
        self.ground_list.draw()
        self.path_list.draw()
        self.patch_list.draw()
        
        self.pathSprite.draw()
        
def main():
    MyGameWindow(1280,720,'CASTLE HALLOWS')
    
    arcade.run()
  
main()

