from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, Board
from . import program
import random

# static values
# the size of the board
SIZE = 7
# the max number of turns
MAX_TURNS = 343


class state:
    def __init__(self, color):
        """
        Initialise the state.
        """
        self._board = Board()
        self._turn = self._board.turn_color
        self._color = color
        self._winner = None

    def print_board(self):
        print(self._board.render())

    def get_legal_actions(self):
        """
        This function is used to get the legal actions.
        legal actions: all the positions player can spawn on. All the directions player can spread to.
        have not finished yet.
        """
        # get the color
        color = self._turn
        # get the board
        board = self._board
        # get the actions
        return

    def update(self, action):
        self._board.apply_action(action)

    # random action
    def random_action(self):
        """
        This function is used to get the random action.
        """
        # get 2 random values
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        return SpawnAction(HexPos(x, y))

