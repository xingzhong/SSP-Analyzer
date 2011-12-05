import networkx as nx
import pygraphviz as pgv
import numpy as np

class Weight:
    def __init__(self, deg):
        self.w = {}
        self.deg = deg
    def new(self, kind):
        if self.w.has_key(kind):
            pass
        else:
            self.w[kind] = self.tpl(kind)

    def tpl(self, type):
        if type == "BinaryOperator":
            zero = np.zeros(self.deg)
            zero[0] = 1
            zero[1] = -1
        elif type.endswith("Stmt") or type == "root":
            zero = np.ones(self.deg)
        else:
            zero = np.zeros(self.deg)
            zero[0] = 1
        return zero
        

class Graph:
    def __init__(self, raw):
        self.net = nx.DiGraph()
        self.candi = []

        for x in raw:
            n = Node(x)
            self.net.add_node(n.hash, attr_dict=n.data)
            self.net.add_node(n.father)
            dEdge = {'order':self.net.out_degree(n.father)}
            dEdge['binary'] = 0
            self.net.add_edge(n.father, n.hash, attr_dict=dEdge)
            if self.is_candi(n):
                self.candi.append(n.data['spell'])
        self.root = self.find_root()
        deg = self.net.out_degree()
        self.deg = max(deg.itervalues())
        self.w = Weight(self.deg)
        self.init_weight()
        self.init_input()
        self.forward()
        #self.find_feature()

    def init_weight(self):
        for n,d in self.net.nodes_iter(data=True):
            self.w.new(d['kind'])
        print self.w.w

    def init_input(self):
        self.input = {}
        for n,d in self.net.nodes_iter(data=True):
            if d['kind'] == "DeclRefExpr":
                if not self.input.has_key(d['spell']):
                    self.input[d['spell']] = 1
        input = np.eye(len(self.input))
        ind = 0
        for k in self.input.iterkeys():
            self.input[k] = input[ind]
            ind = ind + 1
        self.dim = ind 
        print self.input

    def forward(self):
        print self.forward_1(self.root)
    
    def set_label(self, node, label):
        self.net.node[node]['label'] = "%s | %s"%(self.net.node[node]['label']\
                ,label)

    def forward_1(self, node):
        kind = self.net.node[node]['kind']
        if self.net.out_degree(node) == 0:
            name = self.net.node[node]['spell']
            if self.input.has_key(name):
                self.set_label(node, self.input[name])
                return self.input[name]
            else:
                self.net.node[node]['label'] = np.zeros(self.dim)
                return np.zeros(self.dim)
        else:
            succ = self.net.successors(node)
            sum = np.zeros(self.dim)
            ind = 0 
            for s in succ:
                ww = self.w.w[kind][ind] * self.forward_1(s)
                sum = sum + ww
                ind = ind + 1
            self.net.node[node]['label'] = sum
            return sum


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

    def find_feature(self):
        self.dest = []
        for n,d in self.net.nodes_iter(data=True):
            if d and d['kind'] == "DeclRefExpr" and d['spell'] in self.candi:
                self.dest.append(n)
                self.net.node[n]['color'] = 'red'
            if d and d['kind'] in ["BinaryOperator", "CompoundAssignOperator"]:
                for out in self.net.out_edges_iter(n, data=True):
                    order = out[2]['order']
                    if (order == 1):
                        binary = -1
                    else:
                        binary = 1
                    out[2]['binary'] = binary

        feature = map(lambda x: nx.dijkstra_path_length(\
                self.net, source=self.root, target=x, weight='binary')\
                , self.dest)
        print 'dest:', self.expr(self.dest)
        self.feature = dict(zip(self.dest, feature))
        print 'feature', self.feature
        for n in self.dest:
            self.net.node[n]['label'] = "%s|%s"%(self.net.node[n]['spell'], self.feature[n])
            print self.net.node[n]['label']

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
        
        self.data['label'] = "%s|%s"%(raw[0],raw[1])


    def debug(self):
        print "hash:%s"%(self.hash)
        print "data:%s"%(self.data)

