import os
import sqlite3

# TABLE NAME
TABLE_NAME_USER = 'user'

# COLUMN TYPE
TEXT = 'TEXT'
INTEGER = 'INTEGER'
REAL = 'REAL'

# COLUMN NAME FOR TABLES
## user
COL_IDX = 'id'
COL_USER_NAME = 'username'
COL_USER_PASSDIGEST = 'passdigest'

# TABLE DEFINITION

## unit
TABLE_DEFINITION_USER = [
    [COL_IDX, INTEGER, 'NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE'],
    [COL_USER_NAME, TEXT, 'NOT NULL'],
    [COL_USER_PASSDIGEST, TEXT, 'NOT NULL']
]

USER_TABLE_IDX = {
    COL_IDX: 0, COL_USER_NAME: 1, COL_USER_PASSDIGEST: 2
}


class Database(object):

    def __init__(self, dbname):
        self.dbname = dbname
        self.db = self.get_db()
        self.init_db()

    def check_table_existence(self, table_name):
        if self.exec_sql_fetchone("SELECT * from sqlite_master where type='table' and name=?", (table_name, )) is not None:
            return True

    def close_db(self):
        self.db.close()

    def commit_db(self):
        self.db.commit()
    
    def create_table_in_db(self, dbname, table, table_definition, primary_key=None):
        """Creates a table in the specified database.

        Args:
            dbname (str):
            table (str): table name
            table_definition (list): multiple list which contains "[COLUMN, TYPE, *dat]"
            primary_key (str): column name for primary key 
        
        """

        if self.check_table_existence(table) is not None:
            return
        
        sql = "CREATE TABLE %s " % table
        sql += "("
        sql += ",\n".join(["%s %s %s" % (d[0], d[1], d[2]) for d in table_definition])
        if primary_key is not None:
            sql += ", PRIMARY KEY (" + primary_key + ")"
        sql += ");"

        self.exec_sql(sql)

    def exec_sql(self, sql, dat=None):
        """Executes an SQL statement

        Args:
            sql (str): The SQL statement to execute
            dat (tuple): The replacement values for the statement
        """
        cur = self.db.cursor()
        if dat is not None:
            ret = cur.execute(sql, dat)
        else:
            ret = cur.execute(sql)
        return ret


    def exec_sql_fetchone(self, sql, dat=None):
        """Executes an SQL statement to receive a single result

        Args:
            sql (str): The SQL statement to execute
        """
        cur = self.db.cursor()
        if dat is not None:
            ret = cur.execute(sql, dat).fetchone()
        else:
            ret = cur.execute(sql).fetchone()
        return ret
    
    def get_column_names(self, table_name):
        """Get column names from table
        
        Args:
            table_name (str):
        
        Return:
            ret (list):
        """
        cur = self.db.cursor()
        cur.execute('SELECT * from ' + table_name)
        ret = [d[0] for d in cur.description]
        return ret

    def init_db(self):
        """Initialize database with dropping existed table and create new one"""
        raise NotImplementedError

    def get_db(self):
        return sqlite3.connect(self.dbname)

class User(Database):

    def __init__(self, dbname):
        super().__init__(dbname)

    def init_db(self):
        self.create_table_in_db(self.dbname, TABLE_NAME_USER, TABLE_DEFINITION_USER)