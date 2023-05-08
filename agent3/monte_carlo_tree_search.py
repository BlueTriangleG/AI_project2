import random
import math
from collections import defaultdict


class MCTS:
    def __init__(self, exploration_weight=1.41):
        self.score = defaultdict(int)  # total reward of each node
        self.visit = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

    # choose the best action
    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.score[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.score[n] / self.visit[n]  # average reward

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)  # *
        leaf = path[-1]
        self._expand(leaf)  # *
        reward = self._simulate(leaf)  # *
        self._backpropagate(path, reward)

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:  # 如果当前节点不在children字典中，或者当前节点的子节点为空（没有子节点）
                print('node not in children or not self.children[node]')
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
        self.children[node] = node.find_children()  # 加入children字典， 同时在value总加入它的所有的子节点 *

    def _simulate(self, node):  # 返回本次模拟对于当前玩家来说赢了还是输了
        "Returns the reward for a random simulation (to completion) of `node`"
        return node.rollout()

    def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.visit[node] += 1
            self.score[node] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.visit[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.score[n] / self.visit[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.visit[n]
            )

        return max(self.children[node], key=uct)  # 从当前节点的所有子节点中选取一个uct值最大的节点

    def print_tree(self):
        for children in self.children:
            print('children: ', children)
            print('score: ', self.score[children])
            print('visit: ', self.visit[children])
            print('---------------------')

    # delete the key that will never use
    def remove_items_before_key(self, target_key):
        keys_to_remove = []
        for key in self.children.keys():
            if key == target_key:
                break
            keys_to_remove.append(key)
        print('keys_to_remove: ', keys_to_remove)
        for key in keys_to_remove:
            del self.children[key]


"""
def check_tree(root: Node):
    print('root.depth: ', root.depth, 'root.score: ', root.score, 'root.visits: ', root.visits)
    print('root.ucb1()\n: ', root.ucb1(), 'node number: ', len(root.children))
    print('root.action: ', root.action)
    print('root.board: ', root.state.print_board())
    for child in root.children:
        check_tree(child)
    pass

"""
