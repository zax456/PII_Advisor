import pymysql
from pprint import pprint
import configparser
import datetime as dt

class db_connection():

    def __init__(self): 
        self._config = configparser.ConfigParser()
        self._config.read('Software_Engineering/database_config.ini')

        # setting up the connection to database
        self._conn = pymysql.connect(host = self._config.get('rds_database', 'host'), 
                                        user = self._config.get('rds_database', 'user'), 
                                        port = self._config.getint('rds_database', 'port'), 
                                        passwd = self._config.get('rds_database', 'password'), 
                                        db = self._config.get('rds_database', 'dbname')
                                        )

        ## SQL statements
        self.SELECTsql = self._config.get('sql_queries', 'select') %(self._config.get('rds_database', 'tablename'), 
                                                                    self._config.getint('rds_database', 'time_interval'))
        self.DELETEsql = self._config.get('sql_queries', 'truncate') %self._config.get('rds_database', 'tablename')

        self.INSERTsql = self._config.get('sql_queries', 'insert')

        self.UPDATEsql = self._config.get('sql_queries', 'update')


    # function: get all records from jobseekers document table within specific time frame (24 hours)
    # output: tuple of tuples of records
    def _select(self):
        with self._conn:
            cur = self._conn.cursor() # The cursor is used to traverse the records from the result set.
            cur.execute(self.SELECTsql)
            rows = cur.fetchall()
        return rows

    # function - insert newly scanned resumes
    # input: JSON object containing 1) string raw text, 2) dict flagged PIIs, 3) string parsed text, 4) user id
    def insert(self, record):
        with self._conn:
            cur = self._conn.cursor()

            '''
            pick out the available contents
            insert record with contents into the right columns
            `is_deleted` is left out for obvious reason here
            '''
            file_name = record['file_name']
            file_extension = record['file_extension']
            file_size = record['file_size']
            document_category = record['document_category']
            is_default = record['is_default']
            file_path = record['file_path']
            created_by = record['created_by']
            created_on = record['created_on']
            modified_by = record['modified_by']
            modified_on = record['modified_on']
            parsed_content = record['parsed_content']
            parsed_content_v2 = record['parsed_content_v2']
            individual_id = record['individual_id']

            cur.execute(self.INSERTsql, (individual_id, file_name, file_extension, file_size, 
                                        document_category, is_default, file_path, 
                                        created_by, created_on, modified_by, modified_on,
                                        parsed_content, parsed_content_v2))
            print("inserted sucessfully!")
            self._conn.commit()

    # TODO
    # function: update existing record column(s)
    # input: JSON object - is_default, is_delete, modified_by, modified_on
    def update(self, record):
        '''
        Need more specifications from Joseph on this b4 i start coding
        '''
        pass

    # DELETE all records and reset PK
    # input: string user id
    # output: nil
    def _delete(self):
        with self._conn:
            cur = self._conn.cursor()
            cur.execute(self.DELETEsql)
        print("Table reset sucessfully!")

### ---------------------------------------------------------------------------------------------------------------------------------------
# db = db_connection()
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
# for record in fake_data:
#     db.insert(record)
# db.delete()
# pprint(db.select_test())