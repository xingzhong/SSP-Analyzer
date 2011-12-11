import networkx as nx
import pygraphviz as pgv
import numpy as np
import librn as rn
import ann as rnn

class Graph:
    def __init__(self, raw):
        self.net = nx.DiGraph()
        self.candi = []

        for x in raw:
            n = Node(x)
            self.net.add_node(n.hash, attr_dict=n.data)
            self.net.add_node(n.father)
            dEdge = {'label':self.net.out_degree(n.father)+1}
            self.net.add_edge(n.father, n.hash, attr_dict=dEdge)
            if self.is_candi(n):
                self.candi.append(n.data['spell'])

        self.root = self.find_root()
        #deg = self.net.out_degree()
        #self.deg = max(deg.itervalues())
        #self.nn = rn.RN(self.deg)
        #self.init_input()
        #self.nn.training(self)
        rnn.RNN(self.net, self.root)

    def init_input(self):
        self.input = {}
        for n,d in self.net.nodes_iter(data=True):
            if d['kind'] == "DeclRefExpr":
                if not self.input.has_key(d['spell']):
                    self.input[d['spell']] = 1
            self.nn.addNet(d['kind'])

        input = np.eye(len(self.input))
        ind = 0
        for k in self.input.iterkeys():
            self.input[k] = input[ind]
            ind = ind + 1
        self.dim = ind 

    def forward(self):
        return self.forward_1(self.root)
    
    def set_label(self, node, label):
        if self.net.node[node].has_key('label'):
            self.net.node[node]['label'] = "{%s|%s}"%\
                    (self.net.node[node]['label'],label)
        else:
            self.net.node[node]['label'] = label

    def forward_1(self, node):
        kind = self.net.node[node]['kind']
        if self.net.out_degree(node) == 0:
            name = self.net.node[node]['spell']
            if self.input.has_key(name):
                self.set_label(node, self.input[name])
                self.net.node[node]['feature'] = self.input[name]
                return self.input[name]
            else:
                self.set_label(node, np.zeros(self.dim))
                self.net.node[node]['feature'] = np.zeros(self.dim)
                return np.zeros(self.dim)
        else:
            succ = self.get_succ(node)
            input = np.matrix(map(self.forward_1, succ)).getT()
            sum = self.nn.forward(input, kind)
            self.set_label(node, sum)
            self.net.node[node]['feature'] = sum
            return sum
    
    def get_succ(self, node):
        edge = self.net.out_edges(node, data=True)
        edge = sorted(edge)
        succ = map(lambda x: x[1], edge)
        return succ
        

    def is_candi(self, node):
        if node.data['kind'] == "ParmDecl":
            return True
        else :
            return False
        
    def find_root(self):
        sort = nx.topological_sort(self.net)
        d = {'hash':sort[0], 'kind':'root', 'spell':''}
        self.net.add_node(sort[0], attr_dict=d)
        return sort[0]

    def expr(self, n):
        return map(lambda x:self.net.node[x]['spell'], n)

    def draw(self, name = None):
        if not name:
            name = "ast"
        name = "%s.png"%name
        A = nx.to_agraph(self.net)
        A.layout(prog = 'dot')
        print "drawing ..."
        A.draw(name)

class Node:
    def __init__(self, raw):
        self.hash = raw[3]
        self.father = raw[4]
        self.data = {}
        self.data['kind'] = raw[0]
        self.data['spell'] = raw[1]
        self.data['type'] = raw[2]
        self.data['hash'] = raw[3]
        self.data['father'] = raw[4]

        self.data['shape'] = 'record'
        self.data['label'] = "%s|%s"%(raw[0],raw[1])


    def debug(self):
        print "hash:%s"%(self.hash)
        print "data:%s"%(self.data)

