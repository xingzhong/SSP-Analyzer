import libsql as sql
import ann as rnn
import libgraph as gr
import numpy as np
import pickle


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
        if num == 0:
            continue
        print type, weight, num
        var = raw_input("Enter Weight: ")
        print var
        vara = np.fromstring(var, sep=' ')
        num2 = len(vara)
        mydict[type] = vara
        print type, mydict[type]
    pkl_file.close()
    return mydict


#dbname = "clang_testnn_filter"
dbname = "clang_testnn_test"
#dbname = "clang_ssp12_test5"
dbname = "clang_feb24test_onefile"
dbname = "clang_feb24test2_dot"
nodedb = rnn.Node(20)
#nodedb.node = loadChange('arg.data')
nodedb.node = load('arg.data')
#nodedb.show()
#save(nodedb.node, 'arg.data')

ins = sql.SQL(dbname)
tbl = ins.tls()
train_times = 20
for i in range(train_times):
    error = []
    for tt in np.random.permutation(len(tbl)):
        t = tbl[tt]
        table = t[0]
        #print '\n\n', table
        ins.tn = table
        raw = ins.ls()
        if not table == "TranslationUnit":
            g = gr.Graph(raw)
            nn = rnn.RNN(g.net, g.root, g, nodedb)
            nn.train(iterations= 50, N=0.4, M=0.05)
            error.append(nn.ioerr)
            print table, nn.ioerr
    print "****\n[%s]%s\n"%(i, np.average(error))

for tt in np.random.permutation(len(tbl)):
    t = tbl[tt]
    table = t[0]
    ins.tn = table
    raw = ins.ls()
    print ""
    print table
    g = gr.Graph(raw)
    nn = rnn.RNN(g.net, g.root, g, nodedb)
    nn.test()
    g.draw(name=table)
#save(nodedb.node, 'arg.data')

nodedb.show()
ins.free()
