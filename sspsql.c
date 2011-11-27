#include "ssp.h"

#define DBNAME  "clang_"
#define DBUSER  "ssp"
#define DBPWD   "ssp"

#define QUERY(x,y) printf("[sql]:%s\n",y);\
    if (mysql_query((x), (y))) \
    printf("Error %u: %s\n", mysql_errno(x), mysql_error(x))

#define HEADER "id BIGINT NOT NULL AUTO_INCREMENT, \
    kind CHAR(64) NOT NULL, spell CHAR(128), \
    type CHAR(64) NOT NULL, hash BIGINT, primary key (id)" 

#define HEAD "kind, spell, type, hash"

const char*
sql_version(){
    return mysql_get_client_info();
}

void
sql_init(MYSQL *conn, char *dbname){
    char *name = malloc(256 * sizeof(char));
    char *query = malloc(256 * sizeof(char));
    strcpy (name, DBNAME);
    strcat (name, dbname);
    sprintf(query, "create database IF NOT EXISTS %s", name);
    if (conn == NULL){printf(" Connection Error\n");}
    if (mysql_real_connect(conn, "localhost", DBUSER, DBPWD, NULL, 0, NULL, 0) == NULL){
        printf("Error %u: %s\n", mysql_errno(conn), mysql_error(conn));
    }
    QUERY(conn, query);
    mysql_select_db(conn, name);
    free(name);
    free(query);
}

void 
sql_close(MYSQL *conn){
    mysql_close(conn);}

void 
sql_create_tbl(MYSQL *conn, char *tblname, unsigned int flag){ 
    char *query = malloc(256 * sizeof(char));
    if (conn == NULL){printf(" Connection Error\n");}
    if(flag == LOST){
        sprintf(query, "drop table IF EXISTS %s", tblname);
        QUERY(conn, query);
    }
    sprintf(query, "create table IF NOT EXISTS %s (%s)", tblname, HEADER);
    QUERY(conn, query);
    free(query);
}

void 
sql_insert(MYSQL *conn, char *tblname, char *content){
    char *query = malloc(512 * sizeof(char));
    if (conn == NULL){printf(" Connection Error\n");}
    sprintf(query, "insert into %s (%s) values (%s)", tblname, HEAD, content);
    QUERY(conn, query);
    free(query);
}

