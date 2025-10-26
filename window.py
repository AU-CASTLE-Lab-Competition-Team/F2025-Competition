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
        super().__init__(width,height,title)
        #super().__init__(fullscreen=True)
        self.set_location(400,200)

        self.cam_center_x = 0
        self.cam_center_y = 0
        self.zoom_scale = 1.0


        arcade.set_background_color(BACKGROUND_COLOR)
        self.camera = Camera2D()

        # logic for spawning in waves
        self.enemy_list = None
        self.spawn_timer = 0.0
        self.spawn_delay = 3.0
        self.enemies_to_spawn = 3

        self.ground_list = None
        self.patch_list = None
        self.pumpkin_list = None
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
        
        self.setup()
        
    def setup(self):
        self.map = arcade.load_tilemap("assets/maps/test_map2bigger.tmx",1)

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
        self.pumpkin_list = self.map.sprite_lists["pumpkins"]
        self.selected_patch_list = self.map.sprite_lists["selected_patch"]
        self.shop_list = self.map.sprite_lists["shop"]
        self.selected_shopitem_list = self.map.sprite_lists["selected_shopitem"]
        self.gate_layer = self.map.sprite_lists["gate_door"]

        self.seed_list = arcade.SpriteList()
        self.health_bar_layer = self.map.sprite_lists["health_bar"]
        
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
        self.selected_patch.append(self.selected_patches['patch1'][2])
        self.curr_patch_num = 0
        print(self.curr_patch_num)

        #Initializing Shop Items for easier control
        self.selected_shopitems = {}
        id = 0
        for shop_tile in self.selected_shopitem_list:
            self.selected_shopitems['shopitem'+str(id)] = shop_tile
            print(shop_tile)
            id += 1
        
        self.selected_shopitem = arcade.SpriteList()
        self.selected_shopitem.append(self.selected_shopitems['shopitem1'])
        self.curr_shopitem_num = 0
        print(self.curr_shopitem_num)

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
        
        self.spawn_enemy()


        # Initializing pumpkin and adding to a list of objects of type pumpkin for testing
        my_test_pumpkin = Pumpkin("assets/images/basic_pumpkin.png",1,1000,700,range=200)
  
        self.spawned_pumpkins = [my_test_pumpkin]
        self.path_list.append(my_test_pumpkin)

        
        

        
    def spawn_enemy(self):
        enemy = Enemy("assets/images/skeleton_enemy.png",
                    SPRITE_SCALING_ENEMY,
                    self.position_list)

        # Set initial location of the enemy at the first point
        enemy.center_x = self.position_list[0][0]
        enemy.center_y = self.position_list[0][1]

        self.enemy_list.append(enemy)
        

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
        self.pumpkin_list.draw()
        self.enemy_list.draw()
        self.shop_list.draw()
        self.selected_shopitem.draw()
        self.gate_layer.draw()
        self.health_bar_layer.draw()


        self.seed_list.draw()
        
                    


    def on_update(self, delta_time):
        self.enemy_list.update()
        self.seed_list.update()

        #timer to properly spawn enemies in waves
        if self.enemies_to_spawn > 0:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_enemy()
                self.enemies_to_spawn -= 1
                self.spawn_timer = 0.0

        for enemy in self.enemy_list:
            if arcade.check_for_collision(enemy,self.gate_door):
                self.gate.collision(1)

        for pumpkin in self.spawned_pumpkins:
            if pumpkin.targeted_enemy and not pumpkin.seed:
                seed = Seed("assets/images/pumpseed.png",scale=5,pumpkin=pumpkin)

                

                self.seed_list.append(seed)
                
                
                if pumpkin.targeted_enemy.health <=0:
                    pumpkin.targeted_enemy.remove_from_sprite_lists()
                    pumpkin.targeted_enemy = None
                
            else:
                pumpkin.target(self.enemy_list)

            #IDEA: First found enemy attack until eliminated, then find next highest x value enemy
            #Keep attacking until eliminated or leaves range
            

    
    def on_key_press(self,key,modifiers):
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
                    self.selected_shopitem.append(self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)])
                except:
                    self.curr_shopitem_num = 0
                    self.selected_shopitem = arcade.SpriteList()
                    self.selected_shopitem.append(self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)])
                
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
                    self.selected_shopitem.append(self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)])
                except:
                    self.curr_shopitem_num = len(self.selected_shopitems)-1
                    self.selected_shopitem = arcade.SpriteList()
                    self.selected_shopitem.append(self.selected_shopitems['shopitem'+str(self.curr_shopitem_num)])
                
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
                    #Adjust Money
                    #save pumpkin to delete later if a new pumpkin is bought on top of it
                    self.patch_full['patch'+str(self.curr_patch_num)] = 1
                    
                elif self.patch_full['patch'+str(self.curr_patch_num)] == 1:
                    print("Patch is full")
                    #Check to see if the pumpkin attempted to place is different than pumpkin there currently
                    #If True do what would happen if patch is 'empty' but delete pumpkin currently there
                
                

 
def main():
    
    window = MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
  
main()

