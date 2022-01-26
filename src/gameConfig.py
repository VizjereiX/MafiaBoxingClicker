import configparser
import ast

class GameConfig:
    CFG_FILENAME = "config.ini"
    DEFAULTS = {
            "BOARD_LOCATION": (1015, 535, 1335, 855),
            "ATK_BTN_POS":  (1040, 900),
            "TICKET_BTN_POS": (1170, 900),
            "ROUND_BTN_POS": (1000, 710),
            "NEWGAME_BTN_POS": (1300, 905),
            "CLICK_PAUSE_PERIOD": 0.1            
        }

    def __init__(self) -> None:
        self.reset()
        try:
            self._config.read(GameConfig.CFG_FILENAME)
        except:
            pass

    def get(self, key) :
        return ast.literal_eval(self._config["DEFAULT"][key])
    
    def set(self, key, value):
        self._config["DEFAULT"][key] = str(value)

    def reset(self):
        self._config = configparser.ConfigParser()
        self._config['DEFAULT'] = GameConfig.DEFAULTS

    def save(self):
        with open(GameConfig.CFG_FILENAME, 'w') as f:
            self._config.write(f)
