import numpy as np
import copy
import keyboard
import pyautogui
import time
import cv2
from PIL import ImageGrab

from src.board import Board
from src.gameConfig import GameConfig

STATE_INGAME = 1
STATE_BEFORE_START = 2
STATE_ROUND_END = 3
STATE_GAME_END = 4

class Game:
    def __init__(self) -> None:
        self.config = GameConfig()
        self.strategy = GameStrategy()
        pyautogui.PAUSE = self.config.get("CLICK_PAUSE_PERIOD")
        pass

    def run(self):
        self.board = Board()
        while(True):
            self.board.reset()
            if keyboard.is_pressed("q"):
                return
            state = self.detectState()
            if (state == STATE_INGAME):
                map = self.board.getTilesMap()
                chain = self.strategy.findBestMove(map)
                self.markChain(chain, map)                
                self.clickNextTicket()
                self.clickDoAttack()
                self.clickNextTicket()
            elif state == STATE_ROUND_END:
                 self.clickNextRound()
                 self.clickNextTicket()
            elif state == STATE_BEFORE_START:
                 self.clickNewGame()
                 self.clickNextRound()
                 self.clickNextTicket()
            else:
                print("noop")
                
            time.sleep(3)
        pass

    def clickNewGame(self):
        self._click("NEWGAME_BTN_POS")


    def clickNextRound(self):
        self._click("ROUND_BTN_POS")

    def clickDoAttack(self):
        self._click("ATK_BTN_POS")

    def clickNextTicket(self):
        self._click("TICKET_BTN_POS")

    def _click(self, config_key):
        pyautogui.click(self.config.get(config_key))
        time.sleep(0.5)

    def markChain(self, chain, map):
        mapLocation = self.config.get("BOARD_LOCATION")
        prev = chain[0]
        prev = map[prev[0]][prev[1]][1:]
        chain = chain[1:]
        pyautogui.moveTo(prev[0] + mapLocation[0], prev[1] + mapLocation[1])
        pyautogui.mouseDown()
        for el in chain:
            nxt = map[el[0]][el[1]][1:]
            pyautogui.moveTo(nxt[0] + mapLocation[0], nxt[1] + mapLocation[1])
        pyautogui.mouseUp()

    def _getBoardImg(self):
        img = ImageGrab.grab(self.config.get("BOARD_LOCATION")).convert("RGB")
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    def detectState(self):
        img = self._getBoardImg()
        self.board.detectTiles(img)
        if self.board.areAllTilesPropagated():
            return STATE_INGAME
        if self.board.areAllTilesEmpty():
            return STATE_BEFORE_START
        return STATE_ROUND_END
            
        
        
class GameStrategy:
    def findBestMove(self, fullMap):
        bestVal = 0
        bestChain = None
        map = np.full((4,4), None)

        for i in (0,1,2,3):
            for j in (0,1,2,3):
                map[i][j] = (fullMap[i][j][0].getTag(), fullMap[i][j][0].getValue())

        for i in (0,1,2,3):
            for j in (0,1,2,3):
                tag, value = map[i][j]
                map[i][j] = (None, 0)
                newChain, newValue = self._getBestMoveChain(map, tag, (i, j))
                if len(newChain) > 0 and value + newValue > bestVal:
                    bestVal = value + newValue
                    bestChain = [(i,j)] + newChain
                map[i][j] = (tag, value)

        return bestChain

    def _getBestMoveChain(self, map, tag, pos):
        bestVal = 0
        bestChain = []
        
        for i in range(max(pos[0] - 1, 0), min(pos[0] + 2, 4)):
          for j in range(max(pos[1] - 1, 0), min(pos[1] + 2, 4)):
                if map[i][j][0] == tag:
                    value = map[i][j][1]
                    mapCopy = copy.deepcopy(map)
                    mapCopy[i][j] = (None, value)
                    newChain, newValue = self._getBestMoveChain(mapCopy, tag, (i,j))
                    if value + newValue > bestVal:
                        bestVal = value + newValue
                        bestChain = [(i,j)] + newChain

        return (bestChain, bestVal)