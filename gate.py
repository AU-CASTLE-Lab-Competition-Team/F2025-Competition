import arcade



class Gate():
    def __init__(self,max_health=5):
        self.health = max_health
        self.max_health = max_health
    
    def collision(self,amount):
        self.health -= amount
        print(f'Gate took {amount} damage, health is now {self.health}.')
        if self.health <= 0:
            print('Game Over')
            self.game_over()
    
    def game_over(self):
        print('Gate has been destroyed.')
            
    