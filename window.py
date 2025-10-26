import arcade
from arcade.camera import Camera2D
import time

from enemy import Enemy
from constants import SPRITE_SCALING_ENEMY, ENEMY_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR

from pumpkin import Pumpkin
from seed import Seed
from gate import Gate


class MyGameWindow(arcade.Window):
    def __init__(self,width,height,title):
        # super().__init__(width,height,title)
        super().__init__(fullscreen=True)
        # self.set_location(400,200)

        self.cam_center_x = 0
        self.cam_center_y = 0
        self.zoom_scale = 1.0


        arcade.set_background_color(BACKGROUND_COLOR)
        self.camera = Camera2D()

        # logic for spawning in waves
        self.enemy_list = None
        self.spawn_timer = 0.0
        self.spawn_delay = 3.0
        self.enemies_to_spawn = 0

        # new wave system
        self.wave_list = [
            {"enemy_type": "skeleton", "spawn_interval": 3.0, "count": 3},
            {"enemy_type": "zombie",   "spawn_interval": 4.0, "count": 5},
            {"enemy_type": "skeleton", "spawn_interval": 2.0, "count": 8},
            {"enemy_type": "vampire",  "spawn_interval": 3.5, "count": 4},
        ]         
        self.current_wave_index = -1
        self.wave_delay = 5.0
        self.wave_timer = 0.0
        self.current_wave_enemy_type = None

        self.music_player = None
        self.background_music = None

        self.ground_list = None
        self.patch_list = None
        self.path_list = None
        self.health_bar_layer = None
        self.enemy_list = None
        self.selected_patch = None
        self.mode = None
        self.curr_patch_num = None
        self.curr_shopitem_num = None
        self.selected_patches = None
        self.gate_list = None
        self.selected_shopitem = None
        self.patch_full = None
        self.gate_layer = None
        self.gate_door = None
        self.gate = None
        self.seed_list = None
        self.pumpkin_list = None
        self.selected_pumpkin = None
        self.upgrade = None
        self.patch_to_pumpkin = None
        self.money = 10
        self.score = 0
        
        self.shop_pumpkins_layer = None
        
        self.setup()
        
    def setup(self):
        self.map = arcade.load_tilemap("assets/maps/test_map2bigger.tmx",1)

        self.background_music = arcade.load_sound("assets/sound/music.mp3")
        self.music_player = arcade.play_sound(self.background_music, loop=True)
        map_width = self.map.width * self.map.tile_width
        map_height = self.map.height * self.map.tile_height
        
        self.cam_center_x = map_width // 2
        self.cam_center_y = map_height // 2

        scale_x = self.width / map_width
        scale_y = self.height / map_height
        self.zoom_scale = min(scale_x, scale_y)

        self.ground_list = self.map.sprite_lists["ground"]
        self.gate_list = self.map.sprite_lists["gate"]
        self.path_list = self.map.sprite_lists["path"]
        self.patch_list = self.map.sprite_lists["patches"]
        self.selected_patch_list = self.map.sprite_lists["selected_patch"]
        self.shop_list = self.map.sprite_lists["shop"]
        self.selected_shopitem_list = self.map.sprite_lists["selected_shopitem"]
        self.gate_layer = self.map.sprite_lists["gate_door"]
        self.shop_pumpkins_layer = self.map.sprite_lists["shop_pumpkins"]
        self.pumpkin_list = arcade.SpriteList()

        self.seed_list = arcade.SpriteList()
        self.health_bar_layer = self.map.sprite_lists["health_bar"]
        self.upgrade = False
        self.patch_to_pumpkin = {}
        #Initializing Patches in dictionaries for easier access and control
        self.patch_full = {}
        self.selected_patches = {}
        id = 0
        for patch in self.patch_list:
            self.patch_full['patch'+str(id)] = 0 #Setup for determining if patch is full or not
            id += 1
        id = 0
        for patch_tile in self.selected_patch_list:
            self.selected_patches['patch'+str(id)] = [patch_tile.center_x,patch_tile.center_y,patch_tile]
            print(patch_tile)
            id += 1
        
        self.selected_patch = arcade.SpriteList()
        self.curr_patch_num = 0
        self.selected_patch.append(self.selected_patches['patch'+str(self.curr_patch_num)][2])
        print(self.curr_patch_num)

        #Initializing Shop Items for easier control
        self.selected_shopitems = {}
        id = 0
        pumpkin_names = ['classic','2','3','4','5','6','7']
        for shop_tile in self.selected_shopitem_list:
            self.selected_shopitems['shopitem'+str(id)] = [shop_tile,pumpkin_names[id]]
            print(shop_tile)
            id += 1
        
        self.selected_shopitem = arcade.SpriteList()
        self.curr_shopitem_num = 0
        self.selected_pumpkin = 'classic'
        self.selected_shopitem.append(self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)][0])
        print(self.curr_shopitem_num)

        #Setup Health Bar
        self.health_bar = arcade.SpriteList()

        for grave in self.health_bar_layer:
            self.health_bar.append(grave)

        #Initialize Gate Door variable for collisions
        self.gate_door = self.gate_layer[0]
        self.gate = Gate()
        #Setting default mode for the arrow key control
        self.mode = "Patches"

        # Enemy setup
        self.enemy_list = arcade.SpriteList()

        self.position_list = [[0, 550], #changed to self/instance variable to reference in another function
                         [450, 550],
                         [454, 250],
                         [850, 250],
                         [854, 550],
                         [1250, 550],
                         [1254, 150],
                         [1450, 150],
                         [1454, 800],
                         ]
        

        self.spawned_pumpkins = []
        # Initializing pumpkin and adding to a list of objects of type pumpkin for testing
        





        
        

        
    def spawn_enemy(self, enemy_type):
        if enemy_type == "skeleton":
            image = "assets/images/skeleton_enemy.png"
        elif enemy_type == "zombie":
            image = "assets/images/zombie_enemy.png"
        elif enemy_type == "vampire":
            image = "assets/images/vampire_enemy.png"
        else:
            image = "assets/images/skeleton_enemy.png"

        enemy = Enemy(image, SPRITE_SCALING_ENEMY, self.position_list) #changed to image variable

        # Set initial location of the enemy at the first point
        enemy.center_x = self.position_list[0][0]
        enemy.center_y = self.position_list[0][1]

        self.enemy_list.append(enemy)
        

    def spawn_waves(self, delta_time):

        # If we're not currently in a wave, try to start the next wave after wave_delay
        if self.current_wave_index == -1:
            # add a delay for the first wave?
            self.current_wave_index = 0
            wave = self.wave_list[self.current_wave_index]
            self.enemies_to_spawn = wave["count"]
            self.spawn_delay = wave["spawn_interval"]
            self.current_wave_enemy_type = wave["enemy_type"]
            self.wave_timer = 0.0
            print(f"Starting Wave 1: {wave}")
            return

        # Handle spawn timing if there are still enemies to spawn in the current wave
        if self.enemies_to_spawn > 0:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_enemy(self.current_wave_enemy_type)
                self.enemies_to_spawn -= 1
                self.spawn_timer = 0.0
            return

        # No more to spawn in this wave. 
        if len(self.enemy_list) > 0:
            return

        # Wave finished, move to next wave after wave_delay.
        # wave_timer counts the delay between waves
        self.wave_timer += delta_time
        if self.wave_timer >= self.wave_delay:
            # Move to next wave if available
            if self.current_wave_index < len(self.wave_list) - 1:
                self.current_wave_index += 1
                wave = self.wave_list[self.current_wave_index]
                self.enemies_to_spawn = wave["count"]
                self.spawn_delay = wave["spawn_interval"]
                self.current_wave_enemy_type = wave["enemy_type"]
                self.wave_timer = 0.0
                self.spawn_timer = 0.0
                print(f"Starting Wave {self.current_wave_index + 1}: {wave}")
            else:
                # No more waves
                print("All waves completed.")
                self.wave_timer = 0.0


    def on_draw(self):
        self.clear()       
        self.camera.position = (self.cam_center_x, self.cam_center_y)
        self.camera.zoom = self.zoom_scale
        self.camera.use()

        self.ground_list.draw()
        self.gate_list.draw()
        self.path_list.draw()
        self.patch_list.draw()
        self.selected_patch.draw()
        self.enemy_list.draw()
        self.shop_list.draw()
        self.selected_shopitem.draw()
        self.gate_layer.draw()
        self.health_bar.draw()
        self.pumpkin_list.draw()
        self.shop_pumpkins_layer.draw()
        
        arcade.draw_text(f'Money: {self.money}', 1810, 960, arcade.color.WHITE, 20,bold=True)
        arcade.draw_text(f'Score: {self.score}', 1810, 910, arcade.color.WHITE, 20,bold=True)


        self.seed_list.draw()
        
                    


    def on_update(self, delta_time):
        self.enemy_list.update(delta_time)
        self.seed_list.update()

        self.spawn_waves(delta_time)  

        for enemy in self.enemy_list:
            if arcade.check_for_collision(enemy,self.gate_door):
                self.gate.collision(1)
                enemy.health -= 100
                self.health_bar.pop()

        for pumpkin in self.spawned_pumpkins:
            if pumpkin.is_shooting:
                print('shooting')
                pumpkin.current_frame += 1
                if pumpkin.current_frame < len(pumpkin.animation):
                    pumpkin.texture = pumpkin.animation[pumpkin.current_frame]
                else:
                    pumpkin.is_shooting = False
                    pumpkin.texture = pumpkin.idle_texture
            if pumpkin.targeted_enemy and not pumpkin.seed:
                seed = Seed("assets/images/pumpseed.png",scale=2,pumpkin=pumpkin)
                pumpkin.fire_animation()
                self.seed_list.append(seed)
          
                if pumpkin.targeted_enemy.health <=0:
                    pumpkin.targeted_enemy.remove_from_sprite_lists()
                    self.money +=1
                    self.score +=1
                    pumpkin.targeted_enemy = None
                
            else:
                pumpkin.target(self.enemy_list)

            #IDEA: First found enemy attack until eliminated, then find next highest x value enemy
            #Keep attacking until eliminated or leaves range
            

    
    def on_key_press(self,key,modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
        if key == arcade.key.RIGHT:
            print("right arrow key pressed")
            if self.mode == "Patches":
                print('key press')
                self.curr_patch_num += 1
                print(self.curr_patch_num)
                try:
                    self.selected_patch = arcade.SpriteList()
                    self.selected_patch.append(self.selected_patches['patch'+str(self.curr_patch_num)][2])
                except:
                    self.curr_patch_num = 0
                    self.selected_patch = arcade.SpriteList()
                    self.selected_patch.append(self.selected_patches['patch'+str(self.curr_patch_num)][2])
            elif self.mode == "Shop":
                print('shop key press')
                self.curr_shopitem_num += 1
                print(self.curr_shopitem_num)
                try:
                    self.selected_shopitem = arcade.SpriteList()
                    self.selected_shopitem.append(self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)][0])
                    self.selected_pumpkin = self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)][1]
                except:
                    self.curr_shopitem_num = 0
                    self.selected_shopitem = arcade.SpriteList()
                    self.selected_shopitem.append(self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)][0])
                    self.selected_pumpkin = self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)][1]
                
        elif key == arcade.key.LEFT:
            print("left arrow key pressed")
            if self.mode == "Patches":
                print('key press')
                self.curr_patch_num -= 1
                print(self.curr_patch_num)
                try:
                    self.selected_patch = arcade.SpriteList()
                    self.selected_patch.append(self.selected_patches['patch'+str(self.curr_patch_num)][2])
                except:
                    self.curr_patch_num = len(self.selected_patches)-1
                    self.selected_patch = arcade.SpriteList()
                    self.selected_patch.append(self.selected_patches['patch'+str(self.curr_patch_num)][2])
            elif self.mode == "Shop":
                print('shop key press')
                self.curr_shopitem_num -= 1
                print(self.curr_shopitem_num)
                try:
                    self.selected_shopitem = arcade.SpriteList()
                    self.selected_shopitem.append(self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)][0])
                    print(self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)][1])
                    self.selected_pumpkin = self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)][1]
                except:
                    self.curr_shopitem_num = len(self.selected_shopitems)-1
                    self.selected_shopitem = arcade.SpriteList()
                    self.selected_shopitem.append(self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)][0])
                    self.selected_pumpkin = self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)][1]
                
        elif key == arcade.key.Q:
            print('q pressed')
            if self.mode == 'Patches':
                print('Swapping to Shop')
                self.mode = 'Shop'
            elif self.mode == 'Shop':
                print('Swapping to Patches')
                self.mode = 'Patches'
        
        elif key == arcade.key.SPACE:
            print('Attempting to Place/Select Pumpkin')
            if self.mode == 'Patches':
                patch_sprite = self.selected_patch
                print(patch_sprite)
                sel_patch_xy = self.selected_patches['patch'+str(self.curr_patch_num)][:2]
                print(sel_patch_xy)
                #print(self.patch_full['patch'+str(self.curr_patch_num)])
                if self.patch_full['patch'+str(self.curr_patch_num)] == 0:
                    print("Patch is empty")
                    #Place selected pumpkin from shop to sel_patch_xy
                    if self.selected_pumpkin == 'classic':
                        if self.money >= 5:
                            pumpkin = Pumpkin("assets/images/basic_pumpkin.png",1,sel_patch_xy[0],sel_patch_xy[1])
                            self.patch_to_pumpkin['patch'+str(self.curr_patch_num)] = pumpkin
                            self.pumpkin_list.append(pumpkin)
                            self.spawned_pumpkins.append(pumpkin)
                            

                            #Adjust Money
                            self.money -= 5

                            #save pumpkin to delete later if a new pumpkin is bought on top of it
                            self.patch_full['patch'+str(self.curr_patch_num)] = 1
                        else:
                            print('You do not have enough money')
                    
                elif self.patch_full['patch'+str(self.curr_patch_num)] == 1:
                    print("Patch is full")
                    #Check to see if the pumpkin attempted to place is different than pumpkin there currently
                    #If True do what would happen if patch is 'empty' but delete pumpkin currently there
                    if self.upgrade == False:
                        self.money -= 3
                        pumpkin = self.patch_to_pumpkin['patch'+str(self.curr_patch_num)]
                        print(pumpkin)
                        pumpkin.upgrade()
                        print('upgrading pumpkin')
                
                

 
def main():
    
    window = MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
  


#main()

