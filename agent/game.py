from typing import List

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, Board
from referee.game.board import CellState
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
        self._action = None

    def print_board(self):
        print(self._board.render())

    def update(self, action):
        self._board.apply_action(action)
        self._action = action

    # random action
    def random_action(self):
        """
        This function is used to get the random action.
        """
        # get the color
        print('action is taken by:', self._board.turn_color)
        # get one random available action
        action = random.choice(get_legal_actions(self))
        return action

    def get_board(self):
        return self._board

    # detect whether the game is over
    def is_terminal(self):
        return self._board.game_over

    # get the winner
    def get_winner(self):
        return self._board.winner_color

    # get last action
    def get_last_action(self):
        if self._action is None:
            print('no action has been taken')
        return self._action

    @property
    def color(self):
        return self._color


def get_legal_actions(CurrState: state) -> List[Action]:
    """
    This function is used to get the legal actions.
    legal actions: all the positions player can spawn on. All the directions player can spread to.
    have not finished yet.
    """
    # get the board
    CurrBoard = CurrState.get_board()
    # get the color
    color = CurrBoard.turn_color
    # get the positions
    positions = CurrBoard._state
    # get the occupied positions
    occupied_positions = get_same_color_list(positions, color)
    # get the legal actions
    legal_actions = []
    # for Spread actions
    for pos in occupied_positions:
        # all the directions around the position
        directions = [HexDir.Down, HexDir.DownLeft, HexDir.DownRight, HexDir.Up, HexDir.UpLeft, HexDir.UpRight]
        for direction in directions:
            legal_actions.append(SpreadAction(pos[0], direction))
    # for Spawn actions
    # all the position on the board that is not occupied when the total power is less than 49
    if CurrBoard._total_power < 49:
        for x in range(SIZE):
            for y in range(SIZE):
                if positions[HexPos(x, y)].player is None:
                    legal_actions.append(SpawnAction(HexPos(x, y)))
    return legal_actions


def get_same_color_list(position_list: dict[HexPos, CellState], color) -> list[(HexPos, CellState)]:
    same_color_list = []
    for pos in position_list:
        if position_list[pos].player == color:
            same_color_list.append((pos, position_list[pos]))
    return same_color_list
