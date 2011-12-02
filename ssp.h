#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <mysql/mysql.h>
#include "clang-c/Index.h"

#define KEEP 0
#define LOST 1
/*the function prototype for clang */
typedef struct {
    MYSQL *conn;
    char *tblName;
    char *dbName;
    char *file;
}SSPD;

const char* get_version(void);
enum CXChildVisitResult ssp_callback(CXCursor, CXCursor, CXClientData);
enum CXChildVisitResult ssp_function(CXCursor, CXCursor, CXClientData);
enum CXChildVisitResult ssp_type(CXCursor, SSPD* );
void debug_cursor(CXCursor);

/*the function prototype for mysql database */
const char* sql_version(void);
void sql_init(MYSQL *, char *);
void sql_close(MYSQL *);
void sql_create_tbl(MYSQL *, char *, unsigned int ); 
void sql_insert(MYSQL *, char *, char *);
