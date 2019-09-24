import pymysql
from pprint import pprint
import configparser
import datetime as dt
import numpy as np
import pandas as pd
import json

class db_connection_WRITE:

    def __init__(self, config_path): 
        self._config = configparser.ConfigParser()
        self._config.read(config_path)

        # setting up the connection to database
        self._conn = pymysql.connect(host = self._config.get('production_separate_db', 'host'), 
                                    user = self._config.get('production_separate_db', 'user'), 
                                    port = self._config.getint('production_separate_db', 'port'), 
                                    passwd = self._config.get('production_separate_db', 'password'), 
                                    db = self._config.get('production_separate_db', 'dbname')
                                    )

        ## SQL statements
        self.SELECTsql_main = self._config.get('production_separate_db', 'select_main')
        self.INSERTsql_main = self._config.get('production_separate_db', 'insert_main')
        self.UPDATEsql_main = self._config.get('production_separate_db', 'update_main')
        self.SELECT_resume = self._config.get('production_separate_db', 'get_resume')

        self.SELECTsql_pii = self._config.get('piis_db', 'select_pii')
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
            
            file_name = record['file_name']
            file_extension = record['file_extension']
            file_size = record['file_size']
            document_category = record['document_category']
            is_default = record['is_default']
            file_path = record['file_path']
            created_by = record['created_by']
            modified_by = record['modified_by']
            parsed_content = record.get('parsed_content', "Nothing here")
            parsed_content_v2 = record['parsed_content_v2']
            individual_id = record['individual_id']

            cur.execute(self.INSERTsql_main %(self._config.get('production_separate_db', 'tablename'), 
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
                    %(self._config.get('production_separate_db', 'tablename'), individual_id, file_name))

        cols = self._config.get('production_separate_db', 'columns').split(',')
        resume = pd.DataFrame( [list(cur.fetchall()[0])], columns=cols)
        return resume
    
    # function: update existing record column(s)
    # input: JSON object - 1) is_default, 2) is_delete, 3) modified_by, 4) modified_on
    def _update_main(self, record):
        '''
        Updates 'is_delete' when user deletes selected resume
        Updates 'is_default' column of current and new default resumes when user changes default resume
        Update 'modified_on' when any updates happens
        '''
        cur = self._conn.cursor()

        individual_id = record['individual_id']
        selected_resume = self._get_resume(record)
        ID = selected_resume['id'].values[0]
        is_default = record.get('is_default', 0)
        is_delete = record.get('is_delete', 0)

        ''' if selected resume is default and is to be deleted, change default resume to the previous resume '''
        if (is_delete == 1):
            # check if selected resume is the default resume
            if selected_resume['is_default'].values[0] == 1:
                # make default to be the previous resume
                cur.execute("UPDATE %s SET is_default = 1 WHERE individual_id = '%s' AND is_default = 0 AND is_deleted <> 1 \
                            ORDER BY created_on DESC LIMIT 1" 
                            %(self._config.get('production_separate_db', 'tablename'), individual_id))

            # delete and un-default selected resume
            cur.execute(self.UPDATEsql_main 
                        %(self._config.get('production_separate_db', 'tablename'), is_default, is_delete, individual_id, ID))

        # Change default resume to selected resume
        elif (is_default == 1):
            # check if selected resume is deleted
            if (selected_resume['is_deleted'].values[0] == 1): 
                return "\nError! You cannot make a deleted resume as your default resume!"

            # update current default resume's is_default = 0
            cur.execute("UPDATE %s SET is_default=0 WHERE individual_id='%s' AND is_default=1" 
                        %(self._config.get('production_separate_db', 'tablename'), individual_id))
            
            # update new default to the selected resume
            cur.execute(self.UPDATEsql_main 
                        %(self._config.get('production_separate_db', 'tablename'), is_default, is_delete, individual_id, ID))

        self._conn.commit()
        return "\nUpdate sucessfully!"

    # TODO
    # function: retrieve all PIIs of uploaded resumes
    # input: Not sure yet...need to discuss with Tony/CY
    def select_pii(self):
        '''
        returns all records in PII table
        '''
        with self._conn:
            cur = self._conn.cursor() # The cursor is used to traverse the records from the result set.
            cur.execute(self.SELECTsql_pii %('pii'))
            rows = cur.fetchall()
        return rows

    # TODO
    # function: insert PIIs of uploaded resumes
    # input: JSON object containing 1) job_id from main table, 2) individual_id (user), 
    #                               3) name, 4) nric, 5) email, 6) phone_number, 7) physical_address
    def insert_pii(self, record):
        '''
        Insert flagged PIIs for uploaded resume
        '''
        with self._conn:
            cur = self._conn.cursor()

            js_documents_id = record['js_documents_id']
            individual_id = record['individual_id']
            pii_json = json.dumps(record['pii_json'])

            cur.execute(self.INSERTsql_pii, (js_documents_id, individual_id, pii_json))
            print("inserted sucessfully into pii talble!")
            self._conn.commit()

    # function: insert logging statements into database
    # input: ran during exceptions called during any of the functions in process_string or convert_to_text
    def _insert_tmp(self, record):
        # return "hello tonyytonggg"
        with self._conn:
            '''
            '''
            cur = self._conn.cursor()

            file_path = record['file_path']
            data = record['data']
            
            cur.execute(self.INSERTsql_tmp %(self._config.get('production_separate_db', 'tablename_2'), file_path, data))

            print("inserted into tmp sucessfully!")
            self._conn.commit()

### ---------------------------------------------------------------------------------------------------------------------------------------
# db = db_connection_WRITE("Software_Engineering/database_WRITE_config.ini")
# db._update_main({"individual_id":"Testing_ID", "file_name":"Testing_PDF2", "is_delete": 1})


# pii_fake_data = [
#     {
#         "js_documents_id": "doc1",
#         "individual_id": "indv1",
#         "pii_json": {
#             "name": "cylee",
#             "nric": "S1234567Z"
#         }
#     },
#     {
#         "js_documents_id": "doc2",
#         "individual_id": "indv2",
#         "pii_json": {
#             "name": "dylansmith",
#             "nric": "S7654321A",
#             "phone": "91115551"
#         }
#     },
# ]

# for record in pii_fake_data:
#     db.insert_pii(record)

# fake_data = [
#     {
#         "individual_id": "Ang Kian Hwee",
#         "file_name": "AngKianHwee",
#         "file_extension": "pdf",
#         "file_size": 3,
#         "document_category": "Secret",
#         "is_default": 1,
#         "file_path": "data_science/unit_tests/sample_resumes/AngKianHwee.pdf",
#         "created_by": "Ang Kian Hwee",
#         "created_on": dt.datetime(2019, 9, 1, 15, 35, 46),
#         "modified_by": "Ang Kian Hwee",
#         "modified_on": dt.datetime(2019, 9, 1, 15, 35, 46),
#         "is_deleted": 0,
#         "parsed_content": "Placeholder contents",
#         "parsed_content_v2": "Ang Kian Hwee Blk123 Choa Chu Kang Loop #02-34 S680341 Email: angkianhwee@u.nus.edu EDUCATION \
#         National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
#         Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
#         Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
#         Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
#         Computational Methods for BA Expected Date of Graduation: December 2019",
#         },
#     {
#         "individual_id": "Lee Chen Yuan",
#         "file_name": "LeeChenYuan",
#         "file_extension": "pdf",
#         "file_size": 3,
#         "document_category": "Secret",
#         "is_default": 1,
#         "file_path": "data_science/unit_tests/sample_resumes/LeeChenYuan.pdf",
#         "created_by": "Lee Chen Yuan",
#         "created_on": dt.datetime(2019, 9, 2, 15, 35, 46),
#         "modified_by": "Lee Chen Yuan",
#         "modified_on": dt.datetime(2019, 9, 3, 15, 35, 46),
#         "parsed_content": "Placeholder contents",
#         "parsed_content_v2": "Lee Chen Yuan Blk456 Yew Tee Cresent #02-34 S890421 Email: leechenyuan@u.nus.edu EDUCATION \
#         National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
#         Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
#         Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
#         Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
#         Computational Methods for BA Expected Date of Graduation: December 2019",
#         },
#     {
#         "individual_id": "Tony Tong",
#         "file_name": "TonyTong",
#         "file_extension": "pdf",
#         "file_size": 3,
#         "document_category": "Secret",
#         "is_default": 1,
#         "file_path": "data_science/unit_tests/sample_resumes/TonyTong.pdf",
#         "created_by": "Tony Tong",
#         "created_on": dt.datetime(2019, 9, 5, 15, 35, 46),
#         "modified_by": "Tony Tong",
#         "modified_on": dt.datetime(2019, 9, 5, 15, 35, 46),
#         "parsed_content": "Placeholder contents",
#         "parsed_content_v2": "Tony Tong Blk789 Bukit Gombak Road #02-34 S652432 Email: tonytong@u.nus.edu EDUCATION \
#         National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
#         Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
#         Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
#         Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
#         Computational Methods for BA Expected Date of Graduation: December 2019",
#         },
#     {
#         "individual_id": "Markus Ng",
#         "file_name": "MarkusNg",
#         "file_extension": "pdf",
#         "file_size": 3,
#         "document_category": "Secret",
#         "is_default": 1,
#         "file_path": "data_science/unit_tests/sample_resumes/MarkusNg.pdf",
#         "created_by": "Markus Ng",
#         "created_on": dt.datetime(2019, 9, 5, 21, 35, 46),
#         "modified_by": "Markus Ng",
#         "modified_on": dt.datetime(2019, 9, 5, 21, 35, 46),
#         "parsed_content": "Placeholder contents",
#         "parsed_content_v2": "Markus Ng Blk123 Kent Ridge #02-34 S119201 Email: markusng@u.nus.edu EDUCATION \
#         National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
#         Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
#         Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
#         Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
#         Computational Methods for BA Expected Date of Graduation: December 2019",
#         }, 
#     {
#         "individual_id": "Sheryl Ker",
#         "file_name": "SherylKer",
#         "file_extension": "pdf",
#         "file_size": 3,
#         "document_category": "Secret",
#         "is_default": 1,
#         "file_path": "data_science/unit_tests/sample_resumes/SherylKer.pdf",
#         "created_by": "Sheryl Ker",
#         "created_on": dt.datetime(2019, 9, 6, 15, 25, 46),
#         "modified_by": "Sheryl Ker",
#         "modified_on": dt.datetime(2019, 9, 8, 15, 25, 46),
#         "parsed_content": "Placeholder contents",
#         "parsed_content_v2": "Sheryl Ker Blk123 Clementi Ave 5 #02-34 S532900 Email: sherylker@u.nus.edu EDUCATION \
#         National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
#         Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
#         Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
#         Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
#         Computational Methods for BA Expected Date of Graduation: December 2019",
#         } 
#     ]