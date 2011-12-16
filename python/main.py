import libsql as sql
import ann as rnn
import libgraph as gr
import numpy as np

#dbname = "clang_testnn_filter"
dbname = "clang_testnn_test"
#dbname = "clang_ssp12_test5"
dbname = "clang_onefile_onefile"
nodedb = rnn.Node(9)
ins = sql.SQL(dbname)
tbl = ins.tls()
train_times = 50
for i in range(train_times):
    error = []
    for tt in np.random.permutation(len(tbl)):
        t = tbl[tt]
        table = t[0]
        ins.tn = table
        raw = ins.ls()
        if not table == "TranslationUnit":
            g = gr.Graph(raw)
            nn = rnn.RNN(g.net, g.root, g, nodedb)
            nn.train(iterations=20, N=0.1, M=0.05)
            error.append(nn.ioerr)
    print "[%s]%s"%(i, np.average(error))

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
    #g.draw(name=table)

nodedb.show()
ins.free()
