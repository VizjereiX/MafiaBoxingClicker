

class GameConfig:
    def __init__(self) -> None:
        pass

    def get(self, key):
        if key == "BOARD_LOCATION":
            return (1015, 535, 1335, 855)
        if key == "ATK_BTN_POS":
            return (1040, 900)
        if key == "TICKET_BTN_POS":
            return (1170, 900)
        if key == "ROUND_BTN_POS":
            return (1000, 710)
        if key == "NEWGAME_BTN_POS":
            return (1300, 905)
        if key == "CLICK_PAUSE_PERIOD":
            return 0.1
        return None
    