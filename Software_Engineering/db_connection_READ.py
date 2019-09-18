import pymysql
from pprint import pprint
import configparser
import datetime as dt

class db_connection_READ:

    def __init__(self, config_path): 
        self._config = configparser.ConfigParser()
        self._config.read(config_path)

        # setting up the connection to database
        self._conn = pymysql.connect(host = self._config.get('production_db', 'host'), 
                                        user = self._config.get('production_db', 'user'), 
                                        port = self._config.getint('production_db', 'port'), 
                                        passwd = self._config.get('production_db', 'password'), 
                                        db = self._config.get('production_db', 'dbname')
                                        )

        ## SQL statements
        # self.SELECTsql = self._config.get('sql_queries', 'select') %(self._config.get('rds_database', 'tablename'), 
        #                                                             self._config.getint('rds_database', 'time_interval'))

        self.SELECTsql = self._config.get('sql_queries', 'select') %(self._config.get('production_db', 'tablename'))


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