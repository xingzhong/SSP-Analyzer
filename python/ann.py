import numpy as np
from numpy import linalg as LA

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

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
            self.node[label]= np.random.uniform(-1.0, 1.0, self.deg)
            self.err[label]= 0

    def c(self, label):
        if self.node.has_key(label):
            return self.node[label]
        else:
            raise ValueError("Error no weight")

    def update(self, label, value, k):
        #print "[label %s] %s -> "%(label, self.node[label]),
        self.node[label][k] = self.node[label][k] + value
        #print self.node[label]

    def clean(self):
        for v in self.err.keys():
            self.err[v] = 0.0

    def show(self):
        for item in self.node.iteritems():
            node = item[0]
            weight = item[1]
            print node, weight
            

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
        print self.input

    def c(self, label):
        if self.input.has_key(label):
            return self.input[label]
        else:
            return np.zeros_like(self.input.values()[0])


class RNN:
    def __init__(self, tree, root, graph):
        self.tree = tree
        self.root = root
        self.nxg = graph
        self.deg = max(self.tree.out_degree().itervalues())
        self.node = Node(self.deg)
        self.input = Input()
        self.ao = {}
        for n,d in self.tree.nodes_iter(data=True):
            self.node.addNode(d['kind'])
            self.input.addNode(d['spell'])
        self.input.fix()
        self.train(targets=[1,0,0,0])


    def train(self, targets, iterations=100, N=0.5, M=0.1):
        # N: learning rate
        # M: Momentum factor
        for i in range(iterations):
            # update one input
            self.update()
            err = self.backPropagate(targets, N, M)
        print targets
        print err
        self.node.show()

    def backPropagate(self, targets, N, M):
        err = targets - self.output
        self.node.err['root'] = err
        self.bp_err(self.root, N, M)
        self.node.clean()
        return LA.norm(err)

    def bp_dw(self, ft, error, ftk):
        res = 2 * error * (1 - ft) * ft * ftk
        return sum(res)


    
    def bp_err(self, node, N, M):
        kind  = self.tree.node[node]['kind']
        error  = self.node.err[kind]
        ft = self.ao[node]
        weight = self.node.c(kind)
        succ = self.succ(node)
        for k in range(len(succ)):
            kind_k  = self.tree.node[succ[k]]['kind']
            ftk = self.ao[succ[k]]
            change =  N * self.bp_dw(ft, error, ftk)
            self.node.update(kind, change, k)
            self.node.err[kind_k] = self.node.err[kind_k] + weight[k] * error
            self.bp_err(succ[k], N, M)


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
