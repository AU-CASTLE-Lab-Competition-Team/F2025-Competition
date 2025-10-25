import arcade

#{\displaystyle d(p,q)={\sqrt {(p_{1}-q_{1})^{2}+(p_{2}-q_{2})^{2}}}.}

def distance(point1,point2):

    return (   (point1.center_x - point2.center_x)**2 + (point1.center_y - point2.center_y)**2   )**0.5

class Pumpkin(arcade.Sprite):
    def __init__(self,image,scale,location_x,location_y,range =10,damage=10, fire_rate =10):

        super().__init__(image, scale)

        # Initializing pumpkin attributes that will be needed for methods
        self.center_x = location_x
        self.center_y = location_y
        self.range = range
        self.damage = damage
        self.fire_rate = fire_rate
        self.upgrade_level = 1
        self.targeted_enemy= None

    def target(self,enemy_list):

        #Needs the ability to check collisions between the range area (drawn object) and a sprite
        # collided_sprites = arcade.check_for_collision_with_list(self.attack_area,enemy_list)
        
        enemies_in_range = []

        for enemy in enemy_list:
            if distance(enemy,self)<self.range:
                enemies_in_range.append(enemy)
        if enemies_in_range:
            
            max_enemy =  enemies_in_range.pop()    
            for enemy in enemies_in_range:
                if enemy.center_x > max_enemy.center_x:
                    max_enemy = enemy

            self.targeted_enemy = max_enemy
        else:
            self.targeted_enemy = None
        

    def shoot(self,max_enemy,window):

        # This logic likely wont work here because the values wont update properly
        
        seed = arcade.Sprite("assets/images/skeleton_enemy.png",2)
        if self.targeted_enemy:
            while seed.center_x != self.targeted_enemy.center_x and seed.center_y != self.targeted_enemy.center_y:

                if seed.center_x < self.targeted_enemy.center_x:
                    seed.center_x += 1
                if seed.center_x > self.targeted_enemy.center_x:
                    seed.center_x -= 1


                if seed.center_y < self.targeted_enemy.center_y:
                    seed.center_y += 1
                if seed.center_y > self.targeted_enemy.center_y:
                    seed.center_y -= 1

            self.targeted_enemy.health-=10
        
            
    def place_me(self):
        pass
    
    def upgrade(self):
        self.upgrade_level +=1

        if self.upgrade_level == 1:
            self.range = 10
            self.damage = 10
            self.fire_rate = 10
