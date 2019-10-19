from flask import Flask, request, jsonify, abort, make_response, json
import pymysql, sys
import datetime as dt
import re
import os
from db_connection_READ import db_connection_READ
from db_connection_WRITE import db_connection_WRITE
import convert_to_text
import process_string
db_function_read = db_connection_READ("database_READ_config.ini")
db_function_write = db_connection_WRITE("database_WRITE_config.ini")

# TEST COMMANDS
# curl -H "Content-type: application/json" -X POST http://192.168.99.100:5000/upload/ -d '{"filepath":"kh_resume_pdf1.pdf"}'
# curl -H "Content-type: application/json" -X POST http://192.168.99.100:5000/update/ -d '{"individual_id": "ID_testingV2", "file_name": "kh_resume_pdf1", "is_default": 0}'
# curl -H "Content-type: application/json" -X GET http://192.168.99.100:5000/cron_scan/ -d '{"time_duration":438}'
# curl -H "Content-type: application/json" -X GET http://192.168.99.100:5000/directory_scan/
# curl -X GET http://0.0.0.0:5000/directory_scan/
# curl -H "Content-type: application/json" -X POST http://0.0.0.0:5000/upload/ -d '{"filepath":"kh_resume_pdf1.pdf"}'

# docker run -p 5000:80 -v path/to/resumes:path/to/dockerapp image_name


## Note list
# users may re-upload their resumes. This generates a new job ID everytime they upload a new resume. 
# How do we link the job ID and the new resume with the same user? 
# Have a column 'user id' that contains each unique user id?

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test_fn():
    # directory = "../data_science/unit_tests/sample_resumes"
    directory = os.getcwd()
    result = {"directory": "It works!"}
    # result = []
    # try:
    #     for dirName, subdirList, fileList in os.walk(directory):
    #         for file in fileList:
    #             result.append(os.path.join(dirName, file))
    # except Exception as e:
    #     tmp = {
    #         "function": "directory_scan",
    #         "data": e
    #         }
    #     db_function_write._insert_tmp(tmp)
    #     return

    return jsonify(result), 201

@app.route('/directory_scan/', methods=['GET'])
def directory_scan():
    # directory = "../data_science/unit_tests/sample_resumes"
    directory = os.getcwd()
    result = {"directory": directory}
    # result = []
    # try:
    #     for dirName, subdirList, fileList in os.walk(directory):
    #         for file in fileList:
    #             result.append(os.path.join(dirName, file))
    # except Exception as e:
    #     tmp = {
    #         "function": "directory_scan",
    #         "data": e
    #         }
    #     db_function_write._insert_tmp(tmp)
    #     return

    return jsonify(result), 201

@app.route('/cron_scan/', methods=['GET'])
def cron_scan():
    try:
        hour = request.json["time_duration"]
        results = db_function_write.select_pii(hour)
        
    except Exception as e:
        tmp = {
            "function": "cron_scan",
            "data": e
            }
        db_function_write._insert_tmp(tmp)
        return

    return jsonify(results), 201

# This function sends the uploaded resume to our scanning and masking functions 
# which will flag out PIIs and mask them inside the resume
# they will return both the flagged PIIs or masked contents back 
# after which, it will generate a job id and store the contents inside the database
# input: operation to be applied on Resume
# output: flagged PIIs, filtered contents, operation type, job id in JSON format
@app.route('/upload/', methods=['POST', 'GET'])
def process_resume():
    try:
        raw_contents = convert_to_text.convert_to_text(request.json["filepath"])

        PIIs, parsed_contents = process_string.process_string(raw_contents)

        full_filename = request.json["filepath"].lower().split('/')[-1]
        filename = full_filename.split('.')[0]
        file_extension = re.findall(r'\.(\w+)', full_filename)[-1]
        individual_id = "ID_testingV2"
        # individual_id = get_user_id() # TO BE Implemented later

        task = {
            "individual_id": individual_id,
            "file_name": filename,
            "file_extension": file_extension,
            "file_size": 3, #how to get file size?
            "document_category": "Secret",
            "is_default": 1,
            "file_path": request.json["filepath"],
            "created_by": individual_id,
            "created_on": dt.datetime.now(),
            "modified_by": individual_id,
            "modified_on": dt.datetime.now(),
            "parsed_content_v2": parsed_contents,
            }

        db_function_write._insert_main(task) # call insert function to insert/update parsed resume into database

        task_pii = {
        "individual_id": individual_id,
        "file_path": request.json["filepath"],
        "pii_json": PIIs,
        "extracted_on": 'NOW()'
        }
    
        db_function_write.insert_pii(task_pii) # call insert function to insert extracted PIIs into database
        
        return jsonify(task), 201

    except Exception as e: 
        tmp = {
            "file_path": request.json["filepath"],
            "data": e
            }
        db_function_write._insert_tmp(tmp)
        return

@app.route('/update/', methods=['POST'])
def update_resume():

    try:
        data = request.get_json()
        is_default = data.get('is_default', 0)
        is_delete = data.get('is_delete', 0)
        filename = data.get('file_name', 0)
        individual_id = data.get('individual_id', "No Name")
        # individual_id = get_user_id() # TO BE Implemented later
        task = {
            "individual_id": individual_id,
            "is_default": is_default,
            "is_delete": is_delete,
            "file_name": filename
        }
    except Exception as e:
        tmp = {
            "function": "update_resume",
            "data": e
        }

    result = db_function_write._update_main(task)

    return result, 201

# Return error 404 in JSON format
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
