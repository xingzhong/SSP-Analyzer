/* sspcl.c */

#include "clang-c/Index.h"
#include <mysql/mysql.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define OUTPUT(x) clang_getCString(x)
#define is_declfun(x) (clang_getCursorKind(x) == CXCursor_FunctionDecl ? 1 : 0)
#define CONTAIN clang_CXCursorSet_contains //if return 0, set contain the cursor
#define INSERT  clang_CXCursorSet_insert

typedef struct {
    unsigned int depth;
    CXCursorSet parmset;
}SSPD;

const char* get_version(void);
enum CXChildVisitResult ssp_callback(CXCursor, CXCursor, CXClientData);
enum CXChildVisitResult ssp_function(CXCursor, CXCursor, CXClientData);
enum CXChildVisitResult ssp_type(CXCursor, SSPD* );
void debug_cursor(CXCursor);

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
    enum CXCursorKind t = clang_getCursorKind(Cursor);
    SSPD *data = (SSPD *)ClientData;
    int *depth = &(data->depth);
    (*depth)++;
    if (clang_isDeclaration(t)){(*depth) = 1;}
    return ssp_type(Cursor, data);
}

enum CXChildVisitResult 
ssp_callback(CXCursor Cursor, CXCursor Parent, CXClientData ClientData){
    SSPD data;
    data.parmset = clang_createCXCursorSet();
    if (is_declfun(Cursor)){
        data.depth = 1;
        debug_cursor(Cursor);
        clang_visitChildren(Cursor, ssp_function, (CXClientData *)(&data));
    }
    clang_disposeCXCursorSet(data.parmset);
    return CXChildVisit_Continue;
}



enum CXChildVisitResult
ssp_type(CXCursor cursor, SSPD *pd){
    enum CXCursorKind t = clang_getCursorKind(cursor);
    debug_cursor(cursor);
    if (clang_isDeclaration(t)){
        printf("decl\n");
        if(t==CXCursor_ParmDecl){
            if(!INSERT(pd->parmset, cursor)){printf("Already\t");}
            printf("Insert\t%d\t", CONTAIN(pd->parmset, cursor));
            debug_cursor(cursor);
        }
    }
    else if (clang_isReference(t)){
        printf("ref\n");
    }
    else if (clang_isExpression(t)){
        printf("exp\n");
        if(t==CXCursor_DeclRefExpr){
            CXCursor c = clang_getCursorReferenced(cursor);
            if(!CONTAIN(pd->parmset, c)){
                printf("Found Parm\t");
                debug_cursor(cursor);
            }
        }
        else if (t == CXCursor_BinaryOperator){
            printf("Found Binary\t");
            //debug_cursor(cursor);
            //clang_visitChildren(cursor, ssp_tree_debug, (CXClientData *)NULL);
        }
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
    CXIndex Index = clang_createIndex(0,0);
    CXTranslationUnit TU = clang_parseTranslationUnit(Index, 0,\
            argv, argc, 0, 0, CXTranslationUnit_None);
    CXCursor root = clang_getTranslationUnitCursor(TU);
    printf("SSP Analyzer based on %s by Xingzhong\n", get_version());
    printf("Database Link %s\n", mysql_get_client_info());
    clang_visitChildren(root, ssp_callback, (CXClientData *)NULL);
    clang_disposeTranslationUnit(TU);
    clang_disposeIndex(Index);
    return 0;
}
