import numpy as np
from numpy import linalg as LA

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
        self.err = {}
        self.deg = deg

    def addNode(self, label):
        if self.node.has_key(label):
            pass
        else:
            # initilized the weight
            # self.node[label]=np.zeros(self.deg)
            self.node[label]=np.ones(self.deg)
            self.err[label]= 0

    def c(self, label):
        if self.node.has_key(label):
            return self.node[label]
        else:
            raise ValueError("Error no weight")

    def update(self, label, value):
        self.node[label] = self.node[label] + value

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
        self.ao = {}
        for n,d in self.tree.nodes_iter(data=True):
            self.node.addNode(d['kind'])
            self.input.addNode(d['spell'])
        self.input.fix()
        self.train(targets=[0,1,0,0])


    def train(self, targets, iterations=1, N=0.5, M=0.1):
        # N: learning rate
        # M: Momentum factor
        for i in range(iterations):
            # update one input
            self.update()
            self.backPropagate(targets, N, M)

    def backPropagate(self, targets, N, M):
        err = targets - self.output
        derr = err * dsigmoid(self.output)
        self.node.err['root'] = derr
        self.bp_err(self.root)
        print LA.norm(err)

    
    def bp_err(self, node):
        kind  = self.tree.node[node]['kind']
        err  = self.node.err[kind]
        weight = self.node.c(kind)
        error = err * weight 
        succ = self.succ(node)
        for i in range(len(succ)):
            kind  = self.tree.node[succ[i]]['kind']
            ao = self.ao[succ[i]]
            derr = dsigmoid(ao) * error
            self.node.err[kind] = self.node.err[kind] + derr
            change = self.node.err[kind] * ao
            self.node.update(kind, change)
            self.bp_err(succ[i])


    def update(self):
        self.output = self.f(self.root)
        self.ao[self.root] = self.output

    def f(self, node):
        spell = self.tree.node[node]['spell']
        kind  = self.tree.node[node]['kind']
        if self.is_leaf(node):
            self.ao[node] = self.input.c(spell)
            return self.ao[node]
        else:
            succ = self.succ(node)
            input = map(self.f, succ)
            weight = self.node.c(kind)
            sum = dot(input, weight)
            self.ao[node] = sigmoid(sum)
            return self.ao[node]


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
