import networkx as nx
import pygraphviz as pgv

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
        self.find_feature()

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
