import arcade

class MyGameWindow(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        self.set_location(400,200)
        self.pathSprite = arcade.Sprite("assets\images/deadgrass_tile.png",center_x=100,center_y=100)
        

    def on_draw(self):
        arcade.start_render()
        
        self.pathSprite.draw()
        
def main():
    MyGameWindow(1280,720,'CASTLE HALLOWS')
    
    arcade.run()
  
main()

