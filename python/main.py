import libsql as sql
import libgraph as gr

dbname = "clang_ssp10_test4"
ins = sql.SQL(dbname)
tbl = ins.tls()
for t in tbl:
    table = t[0]
    ins.tn = table
    raw = ins.ls()
    g = gr.Graph(raw)
    g.draw(name=table)

ins.free()
