import pymysql
from pprint import pprint

# database credentials
host="bt3101.cu5hwpemnxbf.ap-southeast-1.rds.amazonaws.com"
port=3306
dbname="govtech_external"
user="admin"
tablename = "jobseeker_documents"
conn = pymysql.connect(host, user=user, port=port, passwd="capstone123!", db=dbname)

# Ang Kian Hwee Blk123 Choa Chu Kang Loop #02-34 S680341 Email: angkianhwee@u.nus.edu 
# EDUCATION National University of Singapore (NUS) Bachelor of Science (Business Analytics), 
# Honours Aug 2016 – present 25 years old NRIC: S1234567A Relevant Coursework: Data Management, 
# Business and Technical Communication, Application Systems Development for Business Analytics, Regression Analysis, 
# Data Structure & Algorithms (Python, Java), Mining Web Data for Business Insights, Operations Research, Capstone Project, 
# Computational Methods for BA Expected Date of Graduation: December 2019

# SQL statements
SELECTsql = "SELECT * FROM %s" %tablename
DELETEsql = "TRUNCATE TABLE %s" %tablename
INSERTsql = "INSERT INTO jobseeker_documents (individual_id, parsed_content_v2) VALUES (%s, %s)" # will need to add the other columns later
UPDATEsql = "UPDATE {} ".format(tablename)

# will need to add the other columns later
UPSERTsql = "INSERT INTO %s (individual_id, parsed_content_v2) VALUEs (%s, %s) \
                ON DUPLICATE KEY UPDATE parsed_content_v2 = %s"

# get all records from jobseekers document table
# output: tuple of tuples of records
def select():
    with conn:
        cur = conn.cursor() # we create a cursor. The cursor is used to traverse the records from the result set.
        cur.execute(SELECTsql)
        rows = cur.fetchall()
        pprint(rows)
    return rows

# UPSERT - not upskirt :D
# input: JSON object containing 1) string raw text, 2) dict flagged PIIs, 3) string parsed text, 4) user id
def upsert(record):
    with conn:
        cur = conn.cursor()
        
        # check user id is in table
        cur.execute("SELECT * FROM jobseeker_documents WHERE individual_id = %s" %record["individual_id"])
        rows = cur.fetchall()
        if (len(rows) == 0):
            # insert 
            cur.execute(INSERTsql, (record["individual_id"], record["parsed_content_v2"] ) )
        else:
            for key, value in record.items():
                if (key == "individual_id"):
                    continue
                # rest_of_update_str = "SET {} = {} WHERE individual_id = {}".format(key, value, record["individual_id"])
                rest_of_update_str = "SET {} = '{}' WHERE individual_id = '{}'".format(key, str(value), str(record["individual_id"]))
                s = UPDATEsql + rest_of_update_str
                print(s)
                cur.execute(s)

        conn.commit()

# DELETE all records and reset PK
# input: string user id
# output: nil
def delete(individual_id):
    with conn:
        cur = conn.cursor()
        cur.execute("TRUNCATE TABLE %s" %tablename)

# upsert({"individual_id": "5", "parsed_content_v2": "Updated_Text for user id 5"})