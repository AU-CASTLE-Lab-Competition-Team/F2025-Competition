import arcade
from arcade.camera import Camera2D
from constants import SPRITE_SCALING_ENEMY, ENEMY_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR

from window import MyGameWindow
from window import main

def read_from_lboard():

    file = open("leaderboard.txt",'r')

    people = file.readlines()
    
    top_five_list = []
    for person in people:
        name, score = person.split(',')
        top_five_list.append((int(score),name))
    
    file.close()

    top_five_list.sort()

    top_five_list = list(reversed(top_five_list))
    return_list = top_five_list[:5]
    return return_list

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
        arcade.draw_text(f'CASTLE HOLLOWS', self.cam_center_x-300, self.cam_center_y+200, arcade.color.RED, 72, bold=True, align= 'center')


        arcade.draw_text(f'Press space to start:', self.cam_center_x-300, self.cam_center_y, arcade.color.WHITE, 30,bold=True, align= 'center')
        arcade.draw_text(f'Press Esc at ANY point to exit:', self.cam_center_x-300, self.cam_center_y-200, arcade.color.WHITE, 30,bold=True, align= 'center')

        top_five_list = read_from_lboard() 

        arcade.draw_text(f'Leaderboard', self.cam_center_x-700, self.cam_center_y+200, arcade.color.WHITE, 30,bold=True, align= 'center')
        i = 1
        for person in top_five_list:
            score, name = person

            arcade.draw_text(f'{name}: {score}', self.cam_center_x-700, (self.cam_center_y+200-(i*50)), arcade.color.WHITE, 30,bold=True, align= 'center')
            i +=1

        arcade.draw_text(f'L/R Arrow Keys: Switch through patches', -700, -280, arcade.color.GRAY, 20,bold=True)
        arcade.draw_text(f'Q: Toggle shop', -700, -310,                          arcade.color.GRAY, 20,bold=True)
        arcade.draw_text(f'Space: Place vegetable', -700, -340,                       arcade.color.GRAY, 20,bold=True)
        arcade.draw_text(f'Space: Upgrade vegetable (if on a full vegetable patch)', -700, -370, arcade.color.GRAY, 20,bold=True)
        arcade.draw_text(f'Esc: Exit', -700, -400,                                arcade.color.GRAY, 20,bold=True)

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
        window.close()
        main()
    
    
        
  
main_start()


    