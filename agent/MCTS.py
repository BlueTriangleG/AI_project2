import random
import math


class Node:
    def __int__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0

    def ucb1(self, c=1.98):
        if self.visits == 0:
            return math.inf
        exploitation = self.score / self.visits
        exploration = math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + c * exploration

    def select_best_child(self):
        return max(self.children, key=lambda x: x.ucb1())

    def expand(self):
        legal_actions = self.state.get_legal_actions()
        pass

    def is_terminal(self):
        pass

    def select_best_child(self):
        pass

    def rollout(self):
        pass

    def backPropagate(self):
        pass


def MCTS_search(state, iterMax=1000):
    return state.random_action()
    pass
