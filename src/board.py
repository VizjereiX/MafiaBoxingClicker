import cv2
import numpy as np

class Board:
    def __init__(self):
        self._tileTypes = [GameTile("glove", 1), GameTile("knuckle", 3), GameTile("hammer", 5)]
        self.reset()
        pass

    def reset(self):
        self._tiles = np.full((4,4), None)

    def getTilesMap(self):
        return self._tiles


    def detectTiles(self, image):
        tile_w = image.shape[1] // 4
        tile_h = image.shape[0] // 4
        for type in self._tileTypes:
            result = cv2.matchTemplate(type.getResource(), image, cv2.TM_CCOEFF_NORMED)
            yLoc, xLoc = np.where(result > 0.90)

            w = type.getResource().shape[1]
            h = type.getResource().shape[0]

            rectangles = []
            for (x,y) in zip(xLoc, yLoc):
                rectangles.append([x, y, w, h])
                rectangles.append([x, y, w, h])

            rectangles, _ = cv2.groupRectangles(rectangles, 1, 0.1)
            for r in rectangles:
                x = r[0] // tile_w
                y = r[1] // tile_h
                self._tiles[x][y] = (type, r[0] + w//2, r[1] + w //2 )
    
    
    def areAllTilesPropagated(self):
        for i in (0,1,2,3):
            for j in (0, 1,2,3):
                if self._tiles[i][j] is None:
                    return False
        return True
    
    def areAllTilesEmpty(self):
        for i in (0,1,2,3):
            for j in (0, 1,2,3):
                if self._tiles[i][j] is not None:
                    return False
        return True


class GameTile:
    def __init__(self, tag, pointValue) -> None:
        self._tag = tag
        self._pointValue = pointValue
        self._tileImg = cv2.imread("resources/tiles/" + tag + ".jpg", cv2.IMREAD_COLOR)

    def getTag(self):
        return self._tag

    def getValue(self):
        return self._pointValue

    def getResource(self):
        return self._tileImg

class UndefinedStateException(Exception):
    pass
