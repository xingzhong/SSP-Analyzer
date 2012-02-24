
import ann as rnn
import networkx as nx
import pickle
import numpy as np

def traverse(g, s):
	for n in g.successors_iter(s):
		print "[%s]->[%s]"%(getKind(g, s), getKind(g, n))
		traverse(g, n)
		
def getKind(g, nodex):
	return g.node[nodex]['kind']
	
def getRoot(g):
	for n in g.nodes_iter():
		if g.in_degree(n) == 0:
			attrN = {}
			attrN['kind'] = "root"
			attrN['spell'] = ""
			attrN['type'] = "root"
			g.add_node(n, attrN)
			return n
			
def save(dict, file):
    output = open(file, 'w')
    pickle.dump(dict, output)
    output.close()
    
def load(file):
    pkl_file = open(file, 'r')
    mydict = pickle.load(pkl_file)
    pkl_file.close()
    return mydict

def loadChange(file):
    print "loading data ******"
    pkl_file = open(file, 'r')
    mydict = pickle.load(pkl_file)
    for item in mydict.iteritems():
        type = item[0]
        weight = item[1]
        num = len(weight)
        print type, weight, num
        var = raw_input("Enter Weight: ")
        print var
        mydict[type] = np.fromstring(var, sep=' ')
        print type, mydict[type]
    pkl_file.close()
    return mydict

    
G = nx.DiGraph(name='test')

f = open('test.data', 'r')
for line in f:
	attrN = {}
	attrE = {}
	raw = line.split()
	if len(raw) == 5:
		kind = raw[0]
		spell = raw[1]
		type = raw[2]
		hash = raw[3]
		father = raw[4]
	else:
		kind = raw[0]
		spell = ''
		type = raw[1]
		hash = raw[2]
		father = raw[3]
	attrN['kind'] = kind
	attrN['spell'] = spell
	attrN['type'] = type
	G.add_node(hash, attrN)
	if G.has_node(father):
		num = G.out_degree(father) + 1
	else:
		num = 1
	attrE['order'] = num
	G.add_edge(father, hash, attrE)
f.close()

root = getRoot(G)
traverse(G, root)
nodedb = rnn.Node(4)


#nodedb.node = loadChange('arg.data')
nodedb.node = load('arg.data')
#save(nodedb.node, 'arg.data')
#print nodedb.node
nodedb.show()
nn = rnn.RNN(G, root, None, nodedb)
nn.test()
nn.train(iterations=100, N=0.5, M=0.2)
nodedb.show()
nn.test()
#nn.train(iterations=1, N=1, M=1)
#nodedb.show()
