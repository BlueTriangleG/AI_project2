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
        self.action_list = game.get_legal_actions(self.state)
        self.action = None
        self.depth = 0
        self.turn_color = self.state.color

    def ucb1(self, c=1):
        if self.visits == 0:
            return math.inf
        exploitation = self.score / self.visits
        exploration = math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + c * exploration

    # apply one random legal action to the state
    def apply_action(self, action):
        self.state.update(action)
        self.action = action
        self.turn_color = self.state.color

    def select_best_child(self, children: dict):
        max_ucb1 = -math.inf
        best_child = None
        for child, ucb1 in children.items():
            if ucb1 > max_ucb1:
                # ensure the child is available to expand
                if child.action_list or child.is_terminal():
                    max_ucb1 = child.ucb1()
                    best_child = child
        return best_child

    # select
    def select(self, node):
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def expand(self, children: dict):
        # copy current state and update it
        new_state = copy.deepcopy(self.state)
        # create a new node
        child_Node = Node(new_state, self)
        # get and remove action form the action list
        action = random.choice(self.action_list)
        self.action_list.remove(action)
        # update the action down to this node
        child_Node.apply_action(action)
        # update the action_list
        child_Node.action_list = game.get_legal_actions(child_Node.state)
        child_Node.depth = self.depth + 1
        self.children.append(child_Node)
        children[child_Node] = child_Node.ucb1()
        return child_Node

    def find_children(self, CurrNode):
        if CurrNode in self.children:
            return
        for action in self.action_list:
            new_state = copy.deepcopy(self.state)
            new_state.update(action)
            child_Node = Node(new_state, self)
            child_Node.action = action
            child_Node.action_list = game.get_legal_actions(child_Node.state)
            child_Node.depth = self.depth + 1
            self.children.append(child_Node)
        return self.children

    def is_terminal(self):
        return self.state.is_terminal()

    # play the game to the end randomly
    def rollout(self):
        current_state = self.state
        if current_state is not None:
            simulate_state = copy.deepcopy(current_state)
            while not simulate_state.is_terminal():
                simulate_state.random_action()
            if simulate_state.get_winner() == self.state.color:
                return simulate_state.color, 1
            elif simulate_state.get_winner() is None:
                return simulate_state.color, 0
            else:
                return simulate_state.color, 0
        return 0

    def backPropagate(self, result, score):
        current_node = self
        while True:
            current_node.visits += 1
            if current_node.turn_color == result:
                current_node.score += score
            current_node = current_node.parent
            if current_node.parent is None:
                current_node.visits += 1
                if current_node.turn_color == result:
                    current_node.score += score
                break
        pass

    # get last action
    def get_last_action(self):
        return self.action

    # get the best action
    def get_best_action(self):
        max_ucb1 = -math.inf
        best_child = None
        for child in self.children:
            if child.ucb1() > max_ucb1:
                max_ucb1 = child.ucb1()
                best_child = child
        return best_child.get_last_action()


class MCTS:
    def __init__(self, exploration_weight=1):
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

    # choose the best action
    def choose(self, node):
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(Cur_node):
            if Cur_node.visits == 0:
                return float("-inf")  # avoid unseen moves
            return Cur_node.score / Cur_node.visits  # average reward

        max_node = None
        max_score = -math.inf
        for child in self.children[node]:
            child_score = score(child)
            if child_score > max_score:
                max_node = child
                max_score = child_score
        return max_node

    # do rollout
    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = leaf.rollout()
        leaf.backPropagate(reward)

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:  # 如果当前节点不在children字典中，或者当前节点的子节点为空（没有子节点）
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()  # 得到所有当前子节点中尚未加入children的（即未被探索的）集合
            if unexplored:
                n = unexplored.pop()  # 随机选取一个未被探索的子节点
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()  # 加入children字典， 同时在value总加入它的所有的子节点

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)  # 从当前节点的所有子节点中选取一个uct值最大的节点

    def MCTS_search(self, iterMax=100):
        root = Node(self)
        mcts = MCTS()
        for i in range(iterMax):
            mcts.do_rollout(root)
        return mcts.choose(root).get_last_action()


def check_tree(root: Node):
    print('root.depth: ', root.depth, 'root.score: ', root.score, 'root.visits: ', root.visits)
    print('root.ucb1()\n: ', root.ucb1(), 'node number: ', len(root.children))
    print('root.action: ', root.action)
    print('root.board: ', root.state.print_board())
    for child in root.children:
        check_tree(child)
    pass
