import arcade
from arcade.camera import Camera2D
from constants import SPRITE_SCALING_ENEMY, ENEMY_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR


class MyGameWindow(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        self.set_location(400,200)

        self.cam_center_x = 0
        self.cam_center_y = 0
        self.zoom_scale = 1.0


        arcade.set_background_color(BACKGROUND_COLOR)
        self.camera = Camera2D()

        self.title = title

        self.setup()

    def setup(self):
        pass

    