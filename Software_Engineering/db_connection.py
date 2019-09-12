import pymysql
from pprint import pprint
import configparser
import os

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
        self.SELECTsql = self._config.get('sql_queries', 'select') %self._config.get('rds_database', 'tablename')
        self.DELETEsql = self._config.get('sql_queries', 'truncate') %self._config.get('rds_database', 'tablename')
        # self.DELETEsql = "TRUNCATE TABLE jobseeker_documents;"

        # will need to add the other columns later
        self.INSERTsql = self._config.get('sql_queries', 'insert')
        self.UPDATEsql = self._config.get('sql_queries', 'update')

        # will need to add the other columns later
        # self.UPSERTsql = "INSERT INTO %s (individual_id, parsed_content_v2) VALUEs (%s, %s) ON DUPLICATE KEY UPDATE parsed_content_v2 = %s"


    # function: get all records from jobseekers document table
    # output: tuple of tuples of records
    def select(self):
        with self._conn:
            cur = self._conn.cursor() # we create a cursor. The cursor is used to traverse the records from the result set.
            cur.execute(self.SELECTsql)
            rows = cur.fetchall()
        return rows

    # UPSERT - not upskirt :D
    # input: JSON object containing 1) string raw text, 2) dict flagged PIIs, 3) string parsed text, 4) user id
    def upsert(self, record):
        with self._conn:
            cur = self._conn.cursor()
            
            # check user id is in table
            cur.execute("SELECT * FROM jobseeker_documents WHERE individual_id = %s" %record["individual_id"])
            rows = cur.fetchall()
            if (len(rows) == 0):
                # insert 
                cur.execute(self.INSERTsql, (record["individual_id"], record["parsed_content_v2"]))
                print("inserted sucessfully!")
            else:
                for key, value in record.items():
                    if (key == "individual_id"):
                        continue
                    # rest_of_update_str = "SET {} = {} WHERE individual_id = {}".format(key, value, record["individual_id"])
                    # rest_of_update_str = "SET {} = '{}' WHERE individual_id = '{}'".format(key, str(value), str(record["individual_id"]))
                    # s = self.UPDATEsql + rest_of_update_str
                    cur.execute(self.UPDATEsql, 
                                (self._config.get('rds_database', 'tablename'), key, str(value), str(record["individual_id"]) ) )
                    print("Update sucessfully!")

            self._conn.commit()

    # DELETE all records and reset PK
    # input: string user id
    # output: nil
    def delete(self):
        with self._conn:
            cur = self._conn.cursor()
            cur.execute(self.DELETEsql)
        print("Table reset sucessfully!")

# Testing functions
db = db_connection()
fake_data = [{"individual_id": '1', "parsed_content_v2": "Ang Kian Hwee Blk123 Choa Chu Kang Loop #02-34 S680341 Email: angkianhwee@u.nus.edu EDUCATION \
        National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
        Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
        Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
        Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
        Computational Methods for BA Expected Date of Graduation: December 2019"}, 

            {"individual_id": "2", "parsed_content_v2": "Lee Chen Yuan Blk456 Yew Tee Cresent #02-34 S890421 Email: leechenyuan@u.nus.edu EDUCATION \
        National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
        Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
        Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
        Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
        Computational Methods for BA Expected Date of Graduation: December 2019"}, 

            {"individual_id": "3", "parsed_content_v2": "Tony Tong Blk789 Bukit Gombak Road #02-34 S652432 Email: tonytong@u.nus.edu EDUCATION \
        National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
        Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
        Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
        Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
        Computational Methods for BA Expected Date of Graduation: December 2019"}, 

            {"individual_id": "4", "parsed_content_v2": "Markus Ng Blk123 Kent Ridge #02-34 S119201 Email: markusng@u.nus.edu EDUCATION \
        National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
        Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
        Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
        Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
        Computational Methods for BA Expected Date of Graduation: December 2019"}, 

            {"individual_id": "5", "parsed_content_v2": "Sheryl Ker Blk123 Clementi Ave 5 #02-34 S532900 Email: sherylker@u.nus.edu EDUCATION \
        National University of Singapore (NUS) Bachelor of Science (Business Analytics), Honours \
        Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management and Chinese, \
        Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis,\
        Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project,\
        Computational Methods for BA Expected Date of Graduation: December 2019"}]
# for record in fake_data:
#     db.upsert(record)
# db.delete()
# print(db.select())