import libsql as sql
import libgraph as gr

#dbname = "clang_testnn_filter"
dbname = "clang_testnn_test"
ins = sql.SQL(dbname)
tbl = ins.tls()
for t in tbl:
    table = t[0]
    ins.tn = table
    raw = ins.ls()
    print table
    g = gr.Graph(raw)
    g.draw(name=table)

ins.free()
