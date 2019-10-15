import pymysql
from pprint import pprint
import configparser
import datetime as dt
import os

class db_connection_READ:

    def __init__(self, config_path): 
        self._config = configparser.ConfigParser()
        self._config.read(config_path)

        # setting up the connection to database
        self._conn = pymysql.connect(host = os.environ['PROD_HOST'], 
                                        user = os.environ['PROD_USER'], 
                                        port = int(os.environ['PROD_PORT']), # note port number needs to be in INT format, not string in the env variable! 
                                        passwd = os.environ['PROD_PASSWORD'], 
                                        db = os.environ['PROD_DBNAME']
                                        )

        ## SQL statements
        # self.SELECTsql = self._config.get('sql_queries', 'select') %(self._config.get('rds_database', 'tablename'), 
        #                                                             self._config.getint('rds_database', 'time_interval'))

        self.SELECTsql = self._config.get('sql_queries', 'select') %(os.environ['PROD_TABLENAME'])


    # function: get all records from jobseekers document table within specific time frame (24 hours)
    # output: tuple of tuples of records
    def _select(self):
        with self._conn:
            cur = self._conn.cursor() # The cursor is used to traverse the records from the result set.
            cur.execute(self.SELECTsql)
            rows = cur.fetchall()
        return rows

### ---------------------------------------------------------------------------------------------------------------------------------------
# db = db_connection()
# pprint(db.select_test())