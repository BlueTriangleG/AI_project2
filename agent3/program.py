# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction

from . import game
from .monte_carlo_tree_search import MCTS



# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._state = game.state()
        self.tree = MCTS()
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        match self._color:
            case PlayerColor.RED:
                # use the MCTS to get the action
                self.tree.remove_items_before_key(self._state)
                print(len(self.tree.children),'\n\n\n\n\n\n\n\n\n')
                for i in range(100):
                    self.tree.do_rollout(self._state)
                return_node = self.tree.choose(self._state)
                self.tree.print_tree()
                return return_node.get_action()
            case PlayerColor.BLUE:
                # use the MCTS to get the action
                for i in range(10000):
                    self.tree.do_rollout(self._state)
                return_node = self.tree.choose(self._state)
                return return_node.get_action()

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                # update the game
                self._state.update(action)
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                self._state.update(action)
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass
