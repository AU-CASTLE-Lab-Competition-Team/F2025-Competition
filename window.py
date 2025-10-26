import arcade
from arcade.camera import Camera2D
import arcade.gui as gui
import time

from enemy import Enemy
from zombie import Zombie
from vampire import Vampire
from constants import SPRITE_SCALING_ENEMY, SPRITE_SCALING_ZOMBIE, SPRITE_SCALING_VAMPIRE, ENEMY_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR

from pumpkin import Pumpkin
from gourd import Gourd
from seed import Seed
from gate import Gate

from constants import SEED_DAMAGE
from constants import SEED_SPEED
from constants import PUMP_RANGE
from constants import FIRE_RATE
from constants import G_SEED_DAMAGE
from constants import G_SEED_SPEED
from constants import G_PUMP_RANGE
from constants import G_FIRE_RATE


class MyGameWindow(arcade.Window):
    def __init__(self,width,height,title):
        # super().__init__(width,height,title)
        super().__init__(fullscreen=True)
        # self.set_location(400,200)

        self.manager = gui.UIManager()
        self.manager.enable()

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
            {"enemy_type": "zombie",   "spawn_interval": 3.3, "count": 5},
            {"enemy_type": "skeleton", "spawn_interval": 1.5, "count": 10},
            {"enemy_type": "vampire",  "spawn_interval": 3.5, "count": 6},
            {"enemy_type": "zombie",  "spawn_interval": 2.0, "count": 14},
        ]         
        self.current_wave_index = -1
        self.wave_delay = 4.0
        self.wave_timer = 0.0
        self.current_wave_enemy_type = None

        self.show_wave_text = False       # whether to show current wave
        self.wave_text_timer = 0.0 

        self.music_player = None
        self.background_music = None
        self.pew = None
        

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
        self.game_over = False
        
        self.classic_cost = 5
        self.gourd_cost = 8
        self.upgrade_cost = 3
        
        self.shop_pumpkins_layer = None
        
        #self.setup()
    
    def play_pew(self):
        arcade.play_sound(self.pew, loop=False, volume=1)
        
    def setup(self):
        self.map = arcade.load_tilemap("assets/maps/test_map2bigger.tmx",1)

        self.background_music = arcade.load_sound("assets/sound/music.mp3")
        self.music_player = arcade.play_sound(self.background_music, loop=True,volume=.1)
        
        self.pew = arcade.load_sound("assets/sound/pew.mp3")
        map_width = self.map.width * self.map.tile_width
        map_height = self.map.height * self.map.tile_height
        
        self.cam_center_x = map_width // 2
        self.cam_center_y = map_height // 2

        scale_x = self.width / map_width
        scale_y = self.height / map_height
        self.zoom_scale = min(scale_x, scale_y)
        self.go_time = 0

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
        pumpkin_names = ['classic','gourd']
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
            enemy = Enemy(image, SPRITE_SCALING_ENEMY, self.position_list)
        elif enemy_type == "zombie":
            image = "assets/images/zombie_enemy.png"
            enemy = Zombie(image, SPRITE_SCALING_ZOMBIE, self.position_list)
        elif enemy_type == "vampire":
            image = "assets/images/vampire_enemy.png"
            enemy = Vampire(image, SPRITE_SCALING_VAMPIRE, self.position_list)

        # else:
        #     image = "assets/images/skeleton_enemy.png"

        # enemy = Enemy(image, SPRITE_SCALING_ENEMY, self.position_list) #changed to image variable

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
            self.show_wave_text = True
            self.wave_text_timer = 3.0 
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
                self.show_wave_text = True
                self.wave_text_timer = 3.0
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

        arcade.draw_text(f'Wave: {self.current_wave_index + 1}', 1810, 970, arcade.color.WHITE, 20,bold=True)        
        arcade.draw_text(f'Money: ${self.money}', 1810, 930, arcade.color.WHITE, 20,bold=True)
        arcade.draw_text(f'Score: {self.score}', 1810, 890, arcade.color.WHITE, 20,bold=True)
        arcade.draw_text(f'Selecting: {self.selected_pumpkin}', 1810, 150, arcade.color.WHITE, 20,bold=True)
        if self.selected_pumpkin == 'gourd':
            arcade.draw_text(f'Price: ${self.gourd_cost}', 1810, 100, arcade.color.WHITE, 20,bold=True)
            arcade.draw_text(f'Upgrade: ${self.upgrade_cost}', 1810, 75, arcade.color.WHITE, 20,bold=True)
            arcade.draw_text(f'Damage: {G_SEED_DAMAGE}', 1810, 50, arcade.color.WHITE, 20,bold=True)
        elif self.selected_pumpkin == 'classic':
            arcade.draw_text(f'Price: ${self.classic_cost}', 1810, 100, arcade.color.WHITE, 20,bold=True)
            arcade.draw_text(f'Upgrade: ${self.upgrade_cost}', 1810, 75, arcade.color.WHITE, 20,bold=True)
            arcade.draw_text(f'Damage: {SEED_DAMAGE}', 1810, 50, arcade.color.WHITE, 20,bold=True)
        
        arcade.draw_text(f'Esc: Exit', 10, 30, arcade.color.WHITE, 20,bold=True)
        arcade.draw_text(f'L/R Arrow Keys: Switch through patches', 10, 150, arcade.color.WHITE, 20,bold=True)
        arcade.draw_text(f'Q: Toggle shop', 10, 120, arcade.color.WHITE, 20,bold=True)
        arcade.draw_text(f'Space: Place vegetable', 10, 90, arcade.color.WHITE, 20,bold=True)
        arcade.draw_text(f'Space: Upgrade vegetable (if on a full vegetable patch)', 10, 60, arcade.color.WHITE, 20,bold=True)
        


        if self.show_wave_text:
            arcade.draw_text(f'Wave {self.current_wave_index + 1}', 900, 530, arcade.color.RED, 40, bold=True)


        if self.game_over:
            self.game_over = True
            arcade.draw_text(f'GAME OVER', 600, 700, arcade.color.RED, 100, bold=True, align= 'center')


        self.seed_list.draw()
        
                    


    def on_update(self, delta_time):
        self.enemy_list.update(delta_time)
        self.seed_list.update()

        self.spawn_waves(delta_time)  

        # hide and show wave text
        if self.show_wave_text:
            self.wave_text_timer -= delta_time
            if self.wave_text_timer <= 0:
                self.show_wave_text = False

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
            if pumpkin.targeted_enemy and pumpkin.cooldown >= pumpkin.fire_rate:
                self.play_pew()
                seed = Seed("assets/images/pumpseed.png",scale=2.5,pumpkin=pumpkin)
                pumpkin.fire_animation()
                pumpkin.cooldown = 0
                self.seed_list.append(seed)
            else:
                pumpkin.target(self.enemy_list)
            if pumpkin.targeted_enemy:
                if pumpkin.targeted_enemy.health <=0:
                    print('money update')
                    pumpkin.targeted_enemy.remove_from_sprite_lists()
                    self.money +=1
                    self.score +=1
                    pumpkin.targeted_enemy = None
            if pumpkin.cooldown != pumpkin.fire_rate:
                pumpkin.cooldown += 1
                #print(pumpkin.cooldown)

            #IDEA: First found enemy attack until eliminated, then find next highest x value enemy
            #Keep attacking until eliminated or leaves range


        if self.gate.health <= 0:
            self.game_over = True
            # arcade.draw_text(f'GAME OVER', 1000, 700, arcade.color.RED, 72, bold=True, align= 'center')
            self.go_time += 1
            if self.go_time == 300:
                self.close()
                name = str(input('Type your 4 chacter tag: '))

                file = open('leaderboard.txt','a')
                file.write(f'{name}, {self.score}\n')
            
            

                
            

    
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
                        if self.money >= self.classic_cost:
                            pumpkin = Pumpkin("assets/images/basic_pumpkin.png",1,sel_patch_xy[0],sel_patch_xy[1])
                            self.patch_to_pumpkin['patch'+str(self.curr_patch_num)] = pumpkin
                            self.pumpkin_list.append(pumpkin)
                            self.spawned_pumpkins.append(pumpkin)
                            

                            #Adjust Money
                            self.money -= self.classic_cost

                            #save pumpkin to delete later if a new pumpkin is bought on top of it
                            self.patch_full['patch'+str(self.curr_patch_num)] = 1
                        else:
                            print('You do not have enough money')
                    if self.selected_pumpkin == 'gourd':
                        if self.money >= self.gourd_cost:
                            pumpkin = Gourd("assets/images/gourd.png",1,sel_patch_xy[0],sel_patch_xy[1])
                            self.patch_to_pumpkin['patch'+str(self.curr_patch_num)] = pumpkin
                            self.pumpkin_list.append(pumpkin)
                            self.spawned_pumpkins.append(pumpkin)
                            

                            #Adjust Money
                            self.money -= self.gourd_cost

                            #save pumpkin to delete later if a new pumpkin is bought on top of it
                            self.patch_full['patch'+str(self.curr_patch_num)] = 1
                        else:
                            print('You do not have enough money')
                    
                elif self.patch_full['patch'+str(self.curr_patch_num)] == 1:
                    print("Patch is full")
                    #Check to see if the pumpkin attempted to place is different than pumpkin there currently
                    #If True do what would happen if patch is 'empty' but delete pumpkin currently there
                    if self.money >= self.upgrade_cost:
                        if self.upgrade == False:
                            self.money -= self.upgrade_cost
                            pumpkin = self.patch_to_pumpkin['patch'+str(self.curr_patch_num)]
                            print(pumpkin)
                            pumpkin.upgrade()
                            print('upgrading pumpkin')
                
                

 
def main():
    
    window = MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
  


# main()

