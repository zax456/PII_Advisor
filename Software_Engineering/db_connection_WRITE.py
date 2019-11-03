import pymysql
from pprint import pprint
import configparser
import datetime as dt
import numpy as np
import pandas as pd
import json
import ast
import os

class db_connection_WRITE:

    def __init__(self, config_path): 
        self._config = configparser.ConfigParser()
        self._config.read(config_path)

        # setting up the connection to database
        self._conn = pymysql.connect(host = os.environ['PROD_SEP_HOST'], 
                                    user = os.environ['PROD_SEP_USER'], 
                                    port = int(os.environ['PROD_SEP_PORT']), 
                                    passwd = os.environ['PROD_SEP_PASSWORD'], 
                                    db = os.environ['PROD_SEP_DBNAME']
                                    )

        ## SQL statements
        self.SELECTsql_main = self._config.get('production_separate_db', 'select_main')
        self.INSERTsql_main = self._config.get('production_separate_db', 'insert_main')
        self.UPDATEsql_main = self._config.get('production_separate_db', 'update_main')
        self.SELECT_resume = self._config.get('production_separate_db', 'get_resume')

        self.SELECTsql_pii = self._config.get('piis_db', 'select_pii')
        self.SELECTsql_pii_time = self._config.get('piis_db', 'select_pii_time')
        self.INSERTsql_pii = self._config.get('piis_db', 'insert_pii')

        self.INSERTsql_tmp = self._config.get('production_separate_db', 'insert_tmp')  


    # function: get all records from jobseekers document table within specific time frame (24 hours)
    # output: tuple of tuples of records
    def _select_main(self, hours):
        with self._conn:
            cur = self._conn.cursor() # The cursor is used to traverse the records from the result set.
            cur.execute(self.SELECTsql_main %(self._config.get('production_separate_db', 'tablename'), hours))
            rows = cur.fetchall()
        return rows

    # function: insert uploaded resumes
    # input: JSON object containing 1) string raw text, 2) dict flagged PIIs, 3) string parsed text, 4) user id
    def _insert_main(self, record):
        with self._conn:
            '''
            pick out the available contents
            insert record with contents into the right columns
            `is_deleted` is left out for obvious reason here
            '''
            cur = self._conn.cursor()
            
            file_name = record.get('file_name', "")
            file_extension = record.get('file_extension', "")
            file_size = record.get('file_size', "")
            document_category = record.get('document_category', "")
            is_default = record.get('is_default', "")
            file_path = record.get('file_path', "")
            created_by = record.get('created_by', "")
            modified_by = record.get('modified_by', "")
            parsed_content = record.get('parsed_content', "")
            parsed_content_v2 = record.get('parsed_content_v2', "")
            individual_id = record.get('individual_id', "")

            cur.execute(self.INSERTsql_main %(os.environ['PROD_SEP_TABLENAME'], 
                                            individual_id, file_name, file_extension, file_size, 
                                            document_category, is_default, file_path, 
                                            created_by, modified_by,
                                            parsed_content, parsed_content_v2))
            print("inserted sucessfully!")
            self._conn.commit()

    # helper function to retrieve a resume based on individual id and file name
    # input: JSON/dict
    # output: tuple containing 1 resume and its columns separated by ,
    def _get_resume(self, record):
        cur = self._conn.cursor()

        individual_id = record['individual_id']
        file_name = record['file_name']

        cur.execute(self.SELECT_resume 
                    %(os.environ['PROD_SEP_TABLENAME'], individual_id, file_name))

        cols = self._config.get('production_separate_db', 'columns').split(',')
        resume = pd.DataFrame( [list(cur.fetchall()[0])], columns=cols)
        return resume

    def select_pii(self, hour=None):
        '''
        Generates Cron report with statistics on PIIs etc (TBC)
        Input:
            time interveral to extract data from (int)
        Output:
            Dictionary with different statistics of the hard PIIs (more details to be included soon)
        '''
        with self._conn:
            cur = self._conn.cursor() 
            
            if hour != None:
                cur.execute( self.SELECTsql_pii_time %(os.environ['PII_DB_TABLENAME'], hour) )
            else:
                cur.execute( self.SELECTsql_pii %(os.environ['PII_DB_TABLENAME']) )
            rows = cur.fetchall()

            result = {
                "name": 0,
                "nric": 0,
                "email": 0,
                "phone": 0,
                "address": 0
                }
            for row in rows:
                PIIs = ast.literal_eval(row[3])
                for key, value in PIIs.items():
                    if value:
                        result[key] += 1
            
        return result

    # function: insert PIIs of uploaded resumes
    # input: JSON object containing 1) job_id from main table, 2) individual_id (user), 
    #                               3) name, 4) nric, 5) email, 6) phone_number, 7) physical_address
    def insert_pii(self, record):
        '''
        Insert flagged PIIs for uploaded resume
        Input:
            :record: dictionary consisting of
                        :"individual_id": string
                        :"file_path": string
                        :"pii_json": dict of hard PIIs
                        :"extracted_on": datetime
        '''
        with self._conn:
            cur = self._conn.cursor()

            individual_id = record['individual_id']
            file_path = record['file_path']
            pii_json = json.dumps(record['pii_json'])
            
            # print(self.INSERTsql_pii %(os.environ['PII_DB_TABLENAME'], "'" + individual_id + "'", "'" + file_path + "'", "'" + pii_json + "'", extracted_on))
            cur.execute(self.INSERTsql_pii %(os.environ['PII_DB_TABLENAME'], "'" + individual_id + "'", "'" + file_path + "'", "'" + pii_json + "'"))
            
            print("inserted sucessfully into pii table!")
            self._conn.commit()

    # function: insert logging statements into database
    # input: ran during exceptions called during any of the functions in process_string or convert_to_text
    def _insert_tmp(self, record):
        with self._conn:
            '''
            insert error logs into tmp table
            Input:
                :record: dictionary consisting of file path (string), error log (string)
            '''
            cur = self._conn.cursor()
            file_path = str(record['file_path']).strip()
            data = str(record['data']).strip()
            #data = str(record['data'])
            #rint(f'data: {data}')
            
            cur.execute(self.INSERTsql_tmp %(os.environ['PROD_SEP_TABLENAME_2'], "'" + file_path + "'", "'" + data + "'"))

            print("inserted into tmp sucessfully!")
            self._conn.commit()

