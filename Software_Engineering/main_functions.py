from flask import Flask, request, jsonify, abort, make_response
import pymysql

from data_science.unit_tests.convert_to_text import convert_to_text

host="bt3101.cu5hwpemnxbf.ap-southeast-1.rds.amazonaws.com"
port=3306
dbname="govtech_external"
user="admin"

conn = pymysql.connect(host, user=user, port=port, passwd="capstone123!", db=dbname)

with conn:
    cur = conn.cursor()
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")

    rows = cur.fetchall()

    print(rows)

# TEST COMMANDS
# curl POST -d "filepath='data_science/unit_tests/sample_resumes/kh_resume.pdf'&raw_contents=Ang Kian Hwee is the greatest!" 192.168.99.100:5000/upload/

## Note list
# users may re-upload their resumes. This generates a new job ID everytime they upload a new resume. 
# How do we link the job ID and the new resume with the same user? 
# Have a column 'user id' that contains each unique user id?

app = Flask(__name__)

# This function sends the uploaded resume to our scanning and masking functions 
# which will flag out PIIs and mask them inside the resume
# they will return both the flagged PIIs or masked contents back 
# after which, it will generate a job id and store the contents inside the database
# input: operation to be applied on Resume
# output: flagged PIIs, filtered contents, operation type, job id in JSON format
@app.route('/upload/', methods=['POST'])
def read_resume(filepath):
    # conn = db_connect.connect() # connect to database
    # query = conn.execute("select * from employees") # This line performs query and returns json result

    ## Process the raw contents of the document - flagging, masking
    raw_text = convert_to_text(request.files.get(filepath))

    # Insert flagging of PIIs op here

    # Insert masking of PIIs op here

    task = {"raw text": raw_text}
    return jsonify(task), 201

# function to flag out PIIs and mask contents
# input: raw text from document
# output: JSON object with PIIs and Parsed contents
def process_text(contents):
    result = {
        'PIIs': contents['piis'],
        'Parsed contents': contents['raw_contents']
    }
    return result

# Return error 404 in JSON format
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)