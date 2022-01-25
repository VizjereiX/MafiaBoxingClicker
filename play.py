from src.game import Game
import keyboard

game = Game()
while(True):
    if keyboard.is_pressed("a"):
        game.run()
        quit()
