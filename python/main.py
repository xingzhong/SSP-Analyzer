import libsql as sql
import libgraph as gr

#dbname = "clang_testnn_filter"
dbname = "clang_testnn_test"
#dbname = "clang_ssp12_test5"
ins = sql.SQL(dbname)
tbl = ins.tls()
for t in tbl:
    table = t[0]
    ins.tn = table
    raw = ins.ls()
    print table
    if not table == "TranslationUnit":
        g = gr.Graph(raw)
#    g.draw(name=table)

ins.free()
