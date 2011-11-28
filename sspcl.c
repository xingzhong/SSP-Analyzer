/* sspcl.c */

#include "ssp.h"

#define OUTPUT(x) clang_getCString(x)
#define is_declfun(x) (clang_getCursorKind(x) == CXCursor_FunctionDecl ? 1 : 0)
#define CONTAIN clang_CXCursorSet_contains //if return 0, set contain the cursor
#define INSERT  clang_CXCursorSet_insert
#define PREFIX(x) *strchr(x, '.') = '\0'


void 
debug_cursor(CXCursor Cursor){
    CXString s0 = clang_getCursorKindSpelling(clang_getCursorKind(Cursor));
    CXString s1 = clang_getCursorSpelling(Cursor);
    CXString s2 = clang_getTypeKindSpelling( clang_getCursorType(Cursor).kind);
    unsigned int hash = clang_hashCursor(Cursor);
    printf("[%s]:\t%s\t[%s]\t%X\n\n", OUTPUT(s0), OUTPUT(s1), OUTPUT(s2), hash); 
    clang_disposeString(s0);
    clang_disposeString(s1);
    clang_disposeString(s2);

}

char* 
ssp2sql(CXCursor Cursor, CXCursor Parent){
    char *buf = malloc(512*sizeof(char));
    CXString s0 = clang_getCursorKindSpelling(clang_getCursorKind(Cursor));
    CXString s1 = clang_getCursorSpelling(Cursor);
    CXString s2 = clang_getTypeKindSpelling( clang_getCursorType(Cursor).kind);
    unsigned int hash = clang_hashCursor(Cursor);
    unsigned int father = clang_hashCursor(Parent);
    sprintf(buf, "'%s','%s','%s',%u, %u", OUTPUT(s0), OUTPUT(s1), OUTPUT(s2), hash, father);
    clang_disposeString(s0);
    clang_disposeString(s1);
    clang_disposeString(s2);
    return buf;
}

const char*
get_version(){
    return clang_getCString(clang_getClangVersion());
}

enum CXChildVisitResult 
ssp_tree_debug(CXCursor Cursor, CXCursor Parent, CXClientData ClientData){
    debug_cursor(Cursor);
    return CXChildVisit_Recurse;
}

enum CXChildVisitResult 
ssp_function(CXCursor Cursor, CXCursor Parent, CXClientData ClientData){
    SSPD *data = (SSPD *)ClientData;
    char *content = ssp2sql(Cursor, Parent);
    char *tblName = data->tblName;
    sql_insert(data->conn, tblName, content);
    free(content);
    return CXChildVisit_Recurse;
}

enum CXChildVisitResult 
ssp_callback(CXCursor Cursor, CXCursor Parent, CXClientData ClientData){
    SSPD *data = (SSPD *)ClientData;
    if (is_declfun(Cursor)){
        data->tblName = malloc(128*sizeof(char));
        strcpy(data->tblName, OUTPUT(clang_getCursorSpelling(Cursor)));
        sql_create_tbl(data->conn, data->tblName, LOST); 
        clang_visitChildren(Cursor, ssp_function, (CXClientData *)data);
        free(data->tblName);
        return CXChildVisit_Continue;
    }
    else{
        sql_insert(data->conn, "TranslationUnit", ssp2sql(Cursor, Parent));
        return CXChildVisit_Recurse;
    }
}



enum CXChildVisitResult
ssp_type(CXCursor cursor, SSPD *pd){
    enum CXCursorKind t = clang_getCursorKind(cursor);
    debug_cursor(cursor);
    if (clang_isDeclaration(t)){
        printf("decl\n");
    }
    else if (clang_isReference(t)){
        printf("ref\n");
    }
    else if (clang_isExpression(t)){
        printf("exp\n");
    }
    else if (clang_isStatement(t)){
        printf("stmt\n");
    }
    else if (clang_isAttribute(t)){
        printf("attr\n");
    }
    else if (clang_isInvalid(t)){
        printf("inva\n");
    }
    else if (clang_isTranslationUnit(t)){
        printf("TUnit\n");
    }
    else if (clang_isUnexposed(t)){
        printf("Unexp\n");
    }
    else {
        printf("else\n");
    }
    return CXChildVisit_Recurse;
}

int main(int argc, const char **argv) {
    int i;
    SSPD data;
    CXIndex Index = clang_createIndex(0,0);
    CXTranslationUnit TU = clang_parseTranslationUnit(Index, 0,\
            argv, argc, 0, 0, CXTranslationUnit_None);
    CXCursor root = clang_getTranslationUnitCursor(TU);
    char *fileName = OUTPUT(clang_getTranslationUnitSpelling(TU));
    char *dbname = malloc(128 * sizeof(char));
    PREFIX(fileName);
    strcpy(dbname, "test");
    for (i=0; i<argc; i++){
        if (!strcmp(argv[i], "-dbname")){
            strcpy(dbname, argv[i+1]);
        }
    }
    strcat(dbname, "_");
    strcat(dbname, fileName);
    printf("SSP Analyzer based on %s by Xingzhong\n", get_version());
    printf("Linked to %s @ MySQL v.%s\n", dbname, sql_version());
    data.dbName = dbname; 
    data.conn = mysql_init(NULL);
    sql_init(data.conn, data.dbName); 
    sql_create_tbl(data.conn, "TranslationUnit", KEEP);
    clang_visitChildren(root, ssp_callback, (CXClientData *)(&data));
    clang_disposeTranslationUnit(TU);
    clang_disposeIndex(Index);
    free(dbname);
    sql_close(data.conn);
    return 0;
}
