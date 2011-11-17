/* sspcl.c */

#include "clang-c/Index.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define OUTPUT(x) clang_getCString(x)
#define is_declfun(x) (clang_getCursorKind(x) == CXCursor_FunctionDecl ? 1 : 0)

static const char* GetCursorSource(CXCursor Cursor) {
      CXSourceLocation Loc = clang_getCursorLocation(Cursor);
      CXString source;
      CXFile file;
      clang_getExpansionLocation(Loc, &file, 0, 0, 0);
      source = clang_getFileName(file);
      if (!clang_getCString(source)) {
          clang_disposeString(source);
          return "<invalid loc>";
      }
      else {
          const char *b = basename(clang_getCString(source));
          clang_disposeString(source);
          return b;
      }
}




const char* get_version(void);
enum CXChildVisitResult ssp_callback(CXCursor, CXCursor, CXClientData);
void ssp_type(CXCursor);

const char*
get_version(){
    return clang_getCString(clang_getClangVersion());
}

enum CXChildVisitResult 
ssp_function(CXCursor Cursor, CXCursor Parent, CXClientData ClientData){
    printf("//%s\n", GetCursorSource(Cursor));
    printf("[Father]\t");
    ssp_type(Parent);
    printf("\t [Child]\t");
    ssp_type(Cursor);
    return CXChildVisit_Recurse;
}

enum CXChildVisitResult 
ssp_callback(CXCursor Cursor, CXCursor Parent, CXClientData ClientData){
    if (is_declfun(Cursor)){
        ssp_type(Cursor);
        clang_visitChildren(Cursor, ssp_function, (CXClientData *)NULL);
    }
    return CXChildVisit_Continue;
}



void
ssp_type(CXCursor cursor){
    enum CXCursorKind t = clang_getCursorKind(cursor);
    CXString s1 = clang_getCursorKindSpelling(t);
    CXString s2 = clang_getCursorSpelling(cursor);
    CXString s3 = clang_getCursorDisplayName(cursor);
    CXSourceLocation loc = clang_getCursorLocation(cursor);
    int line, column;
    clang_getSpellingLocation(loc, 0, &line, &column, 0);
    printf("%s\t%s\t%s\t%d:%d\n", OUTPUT(s1), OUTPUT(s2), OUTPUT(s3), line, column);
    clang_disposeString(s1);
    clang_disposeString(s2);
    clang_disposeString(s3);
    if (clang_isDeclaration(t)){
    }
    else if (clang_isReference(t)){
    }
    else if (clang_isExpression(t)){
    }
    else if (clang_isStatement(t)){
    }
    else if (clang_isAttribute(t)){
    }
    else if (clang_isInvalid(t)){
    }
    else if (clang_isTranslationUnit(t)){
    }
    else if (clang_isUnexposed(t)){
    }
    else {
    }
}

int main(int argc, const char **argv) {
    CXIndex Index = clang_createIndex(0,0);
    CXTranslationUnit TU = clang_parseTranslationUnit(Index, 0,\
            argv, argc, 0, 0, CXTranslationUnit_None);
    CXCursor root = clang_getTranslationUnitCursor(TU);

    printf("SSP Analyzer based on %s by Xingzhong\n", get_version());
    clang_visitChildren(root, ssp_callback, (CXClientData *)NULL);
    clang_disposeTranslationUnit(TU);
    clang_disposeIndex(Index);
    return 0;
}
