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

        self.SELECTsql = self._config.get('sql_queries', 'select') %(os.environ['PROD_TABLENAME'])
        self.SELECTfile_name_extension = self._config.get('sql_queries', 'jobseeker_documents_id') 


    # function: get all records from jobseekers document table within specific time frame (24 hours)
    # output: tuple of tuples of records
    def _select(self):
        with self._conn:
            cur = self._conn.cursor() # The cursor is used to traverse the records from the result set.
            cur.execute(self.SELECTsql)
            rows = cur.fetchall()
        return rows

    def select_id(self, record):
        with self._conn:
            cur = self._conn.cursor() # The cursor is used to traverse the records from the result set.
            print(self.SELECTfile_name_extension)
            cur.execute(self.SELECTfile_name_extension %(os.environ['PROD_TABLENAME'], int(record)))
            #cur.execute(self.SELECTfile_name_extension %(record))

            rows = cur.fetchall()
        return rows

        #cur.execute(self.SELECTsql_main %(self._config.get('production_separate_db', 'tablename'), hours))
        #cur.execute(self.SELECTsql_main %(self._config.get('production_separate_db', 'tablename'), hours))