import arcade
from arcade.camera import Camera2D
from constants import SPRITE_SCALING_ENEMY, ENEMY_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR

from window import MyGameWindow
from window import main


class start_Window(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(fullscreen=True)
        # self.set_location(400,200)

        self.cam_center_x = 0
        self.cam_center_y = 0
        self.zoom_scale = 1.0


        arcade.set_background_color(arcade.color.BLACK)
        
        self.camera = Camera2D()

        self.title = title
        self.startgame = True

        self.setup()

    def setup(self):
        pass

    def on_draw(self):
        self.clear()       
        self.camera.position = (self.cam_center_x, self.cam_center_y)
        self.camera.zoom = self.zoom_scale
        self.camera.use()

        arcade.draw_text(f'Press space to start:', self.cam_center_x, self.cam_center_y, arcade.color.WHITE, 100,bold=True, align= 'center',)

    def on_key_press(self,key,modifiers):

        if key == arcade.key.ESCAPE:
            self.startgame = False
            arcade.exit()
            

        if key == arcade.key.SPACE:
            arcade.exit()
            
            
            
            


def main_start():
    
    
    window = start_Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Start screen')
    window.setup()
    arcade.run()

    if window.startgame:
        main()
    
        
  
main_start()


    