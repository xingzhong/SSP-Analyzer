import numpy as np
from numpy import linalg as LA

def sigmoid(x):
    #for i in range(len(x)):
    #    if x[i]<1e-100:
    #        x[i] = 0
    temp = np.exp(-x)
    return 1.0 / (1.0 + temp)

def dot(x, y):
    num = min(len(x), len(y))
    return sum(x[i]*y[i] for i in range(num))

class Node:
    def __init__(self, deg):
        self.node = {}      #node type
        self.err = {}
        self.deg = deg
    
    def addNode(self, label):
        if self.node.has_key(label):
            pass
        else:
            # initilized the weight
            print "init %s"%label
            self.node[label]= np.random.uniform(-1.0, 1.0, self.deg)
            self.err[label]= 0.0
    
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
        for v in self.node.keys():
            self.err[v] = 0.0
    
    def show(self):
        for item in self.node.iteritems():
            node = item[0]
            weight = item[1]
            print "[%s]\t%s"%(node, map(lambda x : "%.2f"%x, weight))


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
        for item in self.input.iteritems():
            print "[%s]\t%s"%(item[0], item[1])
    
    def c(self, label):
        if self.input.has_key(label):
            return self.input[label]
        else:
            return np.zeros_like(self.input.values()[0])
    
    def target(self):   #return output label
        return self.input['OUTPUT']
    
    def inference(self, ins): #given a output, return the variable name
        temp = dict(zip(self.input.keys(), ins))
        for item in temp.iteritems():
            print "[%s]\t%s"%(item[0], item[1])
        return max(temp, key=temp.get)



class RNN:
    def __init__(self, tree, root, graph, nodedb):
        self.tree = tree
        self.root = root
        self.nxg = graph
        self.deg = max(self.tree.out_degree().itervalues())
        #self.node = Node(self.deg)
        self.node = nodedb
        self.input = Input()
        self.ao = {}
        for n,d in self.tree.nodes_iter(data=True):
            self.node.addNode(d['kind'])
            self.input.addNode(d['spell'])
        self.input.fix()
    
    def test(self):
        print self.input.inference(self.update())
    
    def train(self, iterations=100, N=0.7, M=0.1):
        # N: learning rate
        # M: Momentum factor
        targets = self.input.target()
        for i in range(iterations):
            # update one input
            self.update()
            self.ioerr = self.backPropagate(targets, N, M)
            print self.ioerr
        print "[targets]", targets
        print self.update()
    
    def backPropagate(self, targets, N, M):
        self.node.clean()
        err = targets - self.output
        self.node.err['root'] = err
        self.bp_err(self.root, N, M)
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
        
        #self.debug(kind, weight, error, ft)
        for k in range(len(succ)):
            kind_k  = self.tree.node[succ[k]]['kind']
            ftk = self.ao[succ[k]]
            change = N * self.bp_dw(ft, error, ftk)
            self.node.update(kind, change, k)
            self.node.err[kind_k] = self.node.err[kind_k]  + M * weight[k] * error
            self.bp_err(succ[k], N, M)
    
    def debug(self, kind, weight, error, ft):
        print "[%s]"%kind
        print "[weight]\t", map(lambda x : "%.2f"%x, weight)
        print "[error]\t",  map(lambda x : "%.2f"%x, error)
        print "[ft]\t", map(lambda x : "%.2f"%x, ft)

    
    def update(self):
        self.output = self.f(self.root)
        self.ao[self.root] = self.output
        return self.output
    
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
