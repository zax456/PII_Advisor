import pymysql
from pprint import pprint
import configparser
import datetime as dt
import os
import time
import config

class db_connection_READ:

    def __init__(self, config_path): 
        self._config = configparser.ConfigParser()
        self._config.read(config_path)
        try:
            # setting up the connection to database
            print('connecting to ' + config.read_db_user + '@' + config.read_db_host + ':' + config.read_db_port + '...')
            self._conn = pymysql.connect(
                host = config.read_db_host,
                port = int(config.read_db_port), # note port number needs to be in INT format, not string in the env variable! 
                user = config.read_db_user, 
                passwd = config.read_db_password,
                db = config.read_db_database
            )
        except:
            # try again after 10 seconds
            print('failed to connect, trying again in 10 seconds...\n')
            time.sleep(10)
            self.__init__(config_path)
            return

        ## SQL statements
        # self.SELECTsql = self._config.get('sql_queries', 'select') %(self._config.get('rds_database', 'tablename'), 
        #                                                             self._config.getint('rds_database', 'time_interval'))

        self.SELECTsql = self._config.get('sql_queries', 'select') %(config.read_db_table)


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