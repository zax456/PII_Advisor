from flask import Flask, request, jsonify, abort, make_response, json
import pymysql, sys
import importlib.util
from db_connection import db_connection
import convert_to_text
import process_string
db_functions = db_connection()

# docker run -v D:/AKH_Folder/Work/University/Year 4 Sem 1/BT3101 Business Analytics Capstone Project/pii/data_science/unit_tests:/usr/src/app first_docker

# helper function to import functions to read PDF and flag/mask resume contents
# def module_from_file(module_name, file_path):
#     spec = importlib.util.spec_from_file_location(module_name, file_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#     return module

# convert pdf to string
# convert_to_text = module_from_file("unit_tests", "data_science/unit_tests/convert_to_text.py")
# flagging and masking 
# process_string = module_from_file("unit_tests", "data_science/unit_tests/process_string.py")
# database functions
# db_functions = module_from_file("Software_Engineering", "Software_Engineering/db_connections.py")

# TEST COMMANDS
# curl POST -d "filepath="D:/AKH_Folder/Work/University/'Year 4 Sem 1'/'BT3101 Business Analytics Capstone Project'/pii/data_science/unit_tests/sample_resumes/kh_resume.pdf"" 192.168.99.100:5000/upload/

# curl -H "Content-type: application/json" -X POST http://192.168.99.100:5000/upload/ -d '{"filepath":"D:/AKH_Folder/Work/University/Year 4 Sem 1/BT3101 Business Analytics Capstone Project/pii/data_science/unit_tests/sample_resumes/kh_resume.pdf"}'

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
def process_resume():

    raw_contents = convert_to_text.convert_to_text(request.json["filepath"])

    PIIs, parsed_contents = process_string.process_string(raw_contents)

    task = {"raw text": raw_contents, 
            "PIIs": PIIs, 
            "parsed_content_v2": parsed_contents} # will need to add in more columns next time. E.g. date scanned

    db_functions.upsert(task) # call upsert function to insert/update parsed resume into database

    return jsonify(task), 201

# Return error 404 in JSON format
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)


# function to flag out PIIs and mask contents
# input: raw text from document
# output: JSON object with PIIs and Parsed contents
# def process_text(contents):
#     result = {
#         'PIIs': "flagged PIIs",
#         'Parsed contents': "parsed text"
#     }
#     return result