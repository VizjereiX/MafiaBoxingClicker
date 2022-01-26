from src.game import Game

import keyboard
import pyautogui as gui
from PIL import ImageGrab, ImageShow, ImageDraw

game = Game()
config = game.config

def drawPoint(draw, config, key):
    pos = config.get(key)
    draw.rectangle((pos[0] -5, pos[1] - 5, pos[0] + 5, pos[1] + 5), width=5, outline=(255, 0, 0))

def locationSave(config, key):
    x, y = gui.position()
    config.set(key, (x,y))

print("Usage:")
print("\t 1 - BOARD_LOCATION left top point")
print("\t 2 - BOARD_LOCATION right bottom point")
print("\t 3 - ATK_BTN_POS button firing attack")
print("\t 4 - TICKET_BTN_POS button where you need to click to consume ticket for 5 new attacks")
print("\t 5 - ROUND_BTN_POS where to click when roudn ends")
print("\t 6 - NEWGAME_BTN_POS where to click to start new game")
print()
print("\t 0 - show screenshot with all locations marked")
print("\t s - save config to file and quit")
print("\t q - quit without saving")




while(True):
    if keyboard.is_pressed("q"):
        quit()
    if keyboard.is_pressed("1"):        
        config.set("BOARD_LOCATION", gui.position() + config.get("BOARD_LOCATION")[2:])
    if keyboard.is_pressed("2"):
        config.set("BOARD_LOCATION", config.get("BOARD_LOCATION")[0:2] + gui.position())
    if keyboard.is_pressed("3"):
        locationSave(config, "ATK_BTN_POS")
    if keyboard.is_pressed("4"):
        locationSave(config, "TICKET_BTN_POS")
    if keyboard.is_pressed("5"):
        locationSave(config, "ROUND_BTN_POS")
    if keyboard.is_pressed("6"):
        locationSave(config, "NEWGAME_BTN_POS")
    if keyboard.is_pressed("s"):
        config.save()
        quit()
    if  keyboard.is_pressed("0"):
        img = ImageGrab.grab().convert("RGB")
        draw = ImageDraw.Draw(img)
        
        drawPoint(draw, config, "TICKET_BTN_POS")
        drawPoint(draw, config, "ATK_BTN_POS")
        drawPoint(draw, config, "ROUND_BTN_POS")
        drawPoint(draw, config, "NEWGAME_BTN_POS")
        draw.rectangle(config.get("BOARD_LOCATION"), width=5, outline=(255, 0, 0))
        ImageShow.show(img)

