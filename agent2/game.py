import copy
from typing import List

from .board import Board
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
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
        self.color = color
        self._winner = None
        self._action = None
        self._game_over = False

    def print_board(self):
        print(self._board.render())

    def update(self, action):
        self._board.apply_action(action)
        self._action = action
        if self._board.game_over:
            self._game_over = True
            self._winner = self._board.winner_color

    # random action
    def random_action(self):
        """
        This function is used to get the random action.
        """
        # get the color
        # get one random available action
        action = random.choice(get_legal_actions(self))
        # update the board
        self.update(action)
        return action

    def get_board(self):
        return self._board

    # detect whether the game is over
    def is_terminal(self):
        return self._game_over

    # get the winner
    def get_winner(self):
        return self._board.winner_color

    # get last action
    def get_last_action(self):
        if self._action is None:
            return None
        return self._action

    # set up action list
    # get action list

    def __deepcopy__(self, memodict={}):
        new_state = state(self.color)
        new_state._board = copy.deepcopy(self._board)
        new_state._turn = self._turn
        new_state._winner = self._winner
        new_state._action = self._action
        return new_state


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
