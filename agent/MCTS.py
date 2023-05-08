import random
import math
from .game import state
from . import game
import copy

class Node:
    def __init__(self, currState: state, parent=None):
        self.state = currState
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0
        self.legal_actions = game.get_legal_actions(self.state)
        self.action = None

    def ucb1(self, c=1.98):
        if self.visits == 0 or self.parent.visits == 0:
            return math.inf
        exploitation = self.score / self.visits
        exploration = math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + c * exploration

    def select_best_child(self):
        max_ucb1 = -math.inf
        best_child = None
        for child in self.children:
            if child.ucb1() > max_ucb1:
                max_ucb1 = child.ucb1()
                best_child = child
        return best_child

    def expand(self):
        action = random.choice(self.legal_actions)
        new_state = copy.deepcopy(self.state)
        new_state.update(action)
        child_Node = Node(new_state, self)
        # update the action down to this node
        child_Node.action = action
        self.children.append(child_Node)
        return child_Node

    def is_terminal(self):
        return self.state.is_terminal()

    # play the game to the end randomly
    def rollout(self):
        current_state = self.state
        if current_state is not None:
            while not current_state.is_terminal():
                action = current_state.random_action()
                current_state.update(action)
            if current_state.get_winner() == self.state.color:
                return 1
            elif current_state.get_winner() is None:
                return 0
            else:
                return 0
        return 0

    def backPropagate(self, score):
        current_node = self
        while current_node.parent is not None:
            current_node.visits += 1
            current_node.score += score
            current_node = current_node.parent
        pass

    # get last action
    def get_last_action(self):
        return self.action


def MCTS_search(Curr_state, iterMax=1000):
    root = Node(Curr_state)
    # start build tree
    for i in range(iterMax):
        # selection
        current_node = root
        while current_node.children != []:
            if not current_node.children:
                break
            current_node = current_node.select_best_child()
        # expansion
        if not current_node.is_terminal():
            current_node = current_node.expand()
        # simulation
        score = current_node.rollout()
        # backpropagation
        current_node.backPropagate(score)
    best_child = root.select_best_child()
    return best_child.get_last_action()
