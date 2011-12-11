import numpy as np

def sigmoid(x):
    return np.tanh(x)

def dsigmoid(x):
    return 1.0 - x**2

def dot(x, y):
    num = min(len(x), len(y))
    return sum(x[i]*y[i] for i in range(num))

class Node:
    def __init__(self, deg):
        self.node = {}
        self.deg = deg

    def addNode(self, label):
        if self.node.has_key(label):
            pass
        else:
            # initilized the weight
            # self.node[label]=np.zeros(self.deg)
            self.node[label]=np.ones(self.deg)

    def c(self, label):
        if self.node.has_key(label):
            return self.node[label]
        else:
            print "Error no weight"

class Input:
    def __init__(self):
        self.input = {}

    def addNode(self, label):
        if self.input.has_key(label) or label in ['']:
            pass
        else:
            self.input[label] = 1

    def fix(self):
        num = len(self.input)
        ma = np.eye(num)
        self.input = dict(zip(self.input.keys(), ma))

    def c(self, label):
        if self.input.has_key(label):
            return self.input[label]
        else:
            return np.zeros_like(self.input.values()[0])


class RNN:
    def __init__(self, tree, root):
        self.tree = tree
        self.root = root
        self.deg = max(self.tree.out_degree().itervalues())
        self.node = Node(self.deg)
        self.input = Input()
        for n,d in self.tree.nodes_iter(data=True):
            self.node.addNode(d['kind'])
            self.input.addNode(d['spell'])
        self.input.fix()

        # update one input
        self.update()

    def train(self):
        pass

    def update(self):
        return self.f(self.root)

    def f(self, node):
        spell = self.tree.node[node]['spell']
        kind  = self.tree.node[node]['kind']
        if self.is_leaf(node):
            return self.input.c(spell)
        else:
            succ = self.succ(node)
            input = map(self.f, succ)
            weight = self.node.c(kind)
            sum = dot(input, weight)
            return sigmoid(sum)


    def is_leaf(self, node):
        if self.tree.out_degree(node) == 0:
            return True
        else:
            return False

    def succ(self, node):
        # return the list of successors with the order
        edge = self.tree.out_edges(node, data=True)
        succ = map(lambda x: x[1], sorted(edge))
        return succ
