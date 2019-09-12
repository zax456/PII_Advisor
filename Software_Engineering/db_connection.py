import pymysql
from pprint import pprint

class db_connection():

    def __init__(self): 
        self.host = "bt3101-govtech.cu5hwpemnxbf.ap-southeast-1.rds.amazonaws.com"
        self.port=3306
        self.dbname="govtech_external"
        self.user="admin"
        self.tablename = "jobseeker_documents"
        self.conn = pymysql.connect(self.host, user=self.user, port=self.port, passwd="capstone123!", db=self.dbname)

            # SQL statements
        self.SELECTsql = "SELECT * FROM %s" %self.tablename
        self.DELETEsql = "TRUNCATE TABLE %s" %self.tablename

        # will need to add the other columns later
        self.INSERTsql = "INSERT INTO jobseeker_documents (individual_id, parsed_content_v2) VALUES (%s, %s)" 
        self.UPDATEsql = "UPDATE {} ".format(self.tablename)

        # will need to add the other columns later
        self.UPSERTsql = "INSERT INTO %s (individual_id, parsed_content_v2) VALUEs (%s, %s) \
                        ON DUPLICATE KEY UPDATE parsed_content_v2 = %s"



    # get all records from jobseekers document table
    # output: tuple of tuples of records
    def select(self):
        with self.conn:
            cur = self.conn.cursor() # we create a cursor. The cursor is used to traverse the records from the result set.
            cur.execute(self.SELECTsql)
            rows = cur.fetchall()
            # pprint(rows)
        return rows

    # UPSERT - not upskirt :D
    # input: JSON object containing 1) string raw text, 2) dict flagged PIIs, 3) string parsed text, 4) user id
    def upsert(self, record):
        with self.conn:
            cur = self.conn.cursor()
            
            # check user id is in table
            cur.execute("SELECT * FROM jobseeker_documents WHERE individual_id = %s" %record["individual_id"])
            rows = cur.fetchall()
            if (len(rows) == 0):
                # insert 
                cur.execute(self.INSERTsql, (record["individual_id"], record["parsed_content_v2"] ) )
                print("inserted sucessfully!")
            else:
                for key, value in record.items():
                    if (key == "individual_id"):
                        continue
                    # rest_of_update_str = "SET {} = {} WHERE individual_id = {}".format(key, value, record["individual_id"])
                    rest_of_update_str = "SET {} = '{}' WHERE individual_id = '{}'".format(key, str(value), str(record["individual_id"]))
                    s = self.UPDATEsql + rest_of_update_str
                    cur.execute(s)
                    print("Update sucessfully!")

            self.conn.commit()

    # DELETE all records and reset PK
    # input: string user id
    # output: nil
    def delete(self, individual_id):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("TRUNCATE TABLE %s" %self.tablename)

# upsert({"individual_id": "5", "parsed_content_v2": "Updated_Text for user id 5"})