import pymysql, sys
from pprint import pprint

sys.path.insert(0, 'data_science/unit_tests')
import convert_to_text

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

individual_id = 1000
test_text = 0
sql = "INSERT INTO jobseeker_documents (individual_id, parsed_content_v2) VALUES (%s, %s)"

with conn:
    cur = conn.cursor() # we create a cursor. The cursor is used to traverse the records from the result set.

    # cur.execute(sql, (str(individual_id), str(test_text) ))
    # test_text += 1
    # individual_id += 1

    # # connection is not autocommit by default. So you must commit to save
    # # your changes.
    # conn.commit()

    # # SELECT
    # cur.execute("SELECT * FROM %s" %tablename)
    # rows = cur.fetchall()

    # conn.close()
    # pprint(rows)