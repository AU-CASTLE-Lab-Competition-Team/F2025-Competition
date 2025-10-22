import arcade

class MyGameWindow(arcade.Window):
    def __init__(self,width,height,title):
        super().__init__(width,height,title)
        self.set_location(400,200)
        
        
        
def main():
    MyGameWindow(1280,720,'CASTLE HALLOWS')
    arcade.run()


main()

