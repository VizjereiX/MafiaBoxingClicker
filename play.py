from src.game import Game
from src.board import Board
import keyboard

game = Game()
while(True):
    if keyboard.is_pressed("a"):
        game.run()
        quit()