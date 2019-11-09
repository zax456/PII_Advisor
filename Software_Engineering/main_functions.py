from flask import Flask, request, jsonify, abort, make_response, json
import pymysql, sys
import datetime as dt
import re
import os
from db_connection_READ import db_connection_READ
from db_connection_WRITE import db_connection_WRITE
import convert_to_text
import process_string
import config
db_function_read = db_connection_READ("database_READ_config.ini")
db_function_write = db_connection_WRITE("database_WRITE_config.ini")

# TEST COMMANDS
# curl -H "Content-type: application/json" -X POST http://192.168.99.100:5000/upload/ -d '{"filepath":"kh_resume_pdf1.pdf"}'
# curl -H "Content-type: application/json" -X POST http://0.0.0.0:5000/upload/ -d '{"filepath":"sample_resumes/kenneth_lu_resume.pdf"}'
# curl -H "Content-type: application/json" -X POST http://192.168.99.100:5000/update/ -d '{"individual_id": "ID_testingV2", "file_name": "kh_resume_pdf1", "is_default": 0}'
# curl -H "Content-type: application/json" -X GET http://192.168.99.100:5000/cron_scan/ -d '{"time_duration":438}'
# curl -H "Content-type: application/json" -X GET http://192.168.99.100:5000/directory_scan/
# curl -X GET http://0.0.0.0:5000/directory_scan/
# curl -X GET http://192.168.99.100:5000/
# curl -H "Content-type: application/json" -X GET http://192.168.99.100:5000/ -d '{"filepath":"./sample_resumes/kh_resume_pdf1.pdf"}'
# curl -H "Content-type: application/json" -X POST http://0.0.0.0:5000/upload/ -d '{"filepath":"kh_resume_pdf1.pdf"}'
# docker run -p 5000:80 -v path/to/resumes:path/to/dockerapp image_name

app = Flask(__name__)

@app.route('/directory_scan/', methods=['GET'])
def directory_scan():
    directory = "sample_resumes/" # Need to put this as an Environment Variable
    
    result = []
    try:
        for dirName, subdirList, fileList in os.walk(directory):
            for file in fileList:
                filepath = os.path.join(dirName, file)
                process_resume(filepath)
                
    except Exception as e:
        tmp = {
            "file_path": "directory_scan function",
            "data": e
            }
        db_function_write._insert_tmp(tmp)
        return

    return "\nFinished scanning resume directory\n", 201
    # return jsonify(result), 201

@app.route('/cron_scan/', methods=['GET'])
def cron_scan():
    try:
        hour = request.json["time_duration"]
        results = db_function_write.select_pii(hour)
        return jsonify(results), 201
        
    except Exception as e:
        tmp = {
            "function": "cron_scan",
            "data": e
            }
        db_function_write._insert_tmp(tmp)
        return

# This function sends the uploaded resume to our scanning and masking functions 
# which will flag out PIIs and mask them inside the resume
# they will return both the flagged PIIs or masked contents back 
# after which, it will generate a job id and store the contents inside the database
# input: operation to be applied on Resume
# output: flagged PIIs, filtered contents, operation type, job id in JSON format
@app.route('/upload/<jobseeker_document_id>', methods=['POST', 'GET'])
def process_resume(jobseeker_document_id):
    try:
        # TONY testing
        #TEST = db_function_read._select()
        #print(f'TEST: {TEST}')
        
        #since input is primary key, we expect only 1 row returned
        result = db_function_read.select_id(jobseeker_document_id) 
        print(f'result: {result}')
        filename, extension = result[0][0], result[0][1]
        raw_contents = convert_to_text.convert_to_text(filename, extension)
        PIIs, parsed_contents = process_string.process_string(raw_contents)

        # in task, many strings are arbitrary fields which may be customised, the key insertion is "parsed_content_v2"
        task = {
            "individual_id": 'admin', 
            "file_name": filename,
            "file_extension": extension,
            "file_size": float(3),
            "document_category": 'restricted',
            "is_default": 1,
            "file_path": '/',
            "created_by": 'admin_name',
            "created_on": dt.datetime.now(),
            "modified_by": 'admin_name_2',
            "modified_on": dt.datetime.now(),
            "parsed_content_v2": parsed_contents,
            }

        # commenting the below line returns the result to the client * might be useful for a quick win
        db_function_write._insert_main(task) # call insert function to insert/update parsed resume into database

        task_pii = {
            "individual_id": 'admin',
            "file_path": '/',
            "pii_json": PIIs
        }
        db_function_write.insert_pii(task_pii) # call insert function to insert extracted PIIs into database
        return str('Success. Parsed contents and PIIs inserted into 2 tables.'), 200

    except Exception as e: 
        # logging error in temporary database
        tmp = {
            "file_path": '/',
            "data": e
                }
        db_function_write._insert_tmp(tmp)
        return str(e), 500

@app.route('/parsed_content/<file_ext>/<file_path>', methods=['GET'])
def get_parsed_content(file_ext, file_path):
    """
    Function:
        Responds with a JSON structure containing 2 keys:
        1. "content"
        2. "piis"

        The "content" key contains the parsed content while the "piis" key
        contains the mapped PIIs

        Call this function to retrieve the parsed content of a pre-existing file
        that the service has access to

    Example:
        curl -H "Content-Type: application/json" "http://localhost:5000/parsed_content/pdf/0001.pdf"
    """
    absolute_path_to_file = os.path.join(config.data_directory, file_path)
    try:
        raw_content = convert_to_text.convert_to_text_with_ext(absolute_path_to_file, file_ext)
    except Exception as exception:
        response = {
            "error": exception.message,
            "params": {
                "file_ext": file_ext,
                "file_path": file_path
            }
        }
        return jsonify(response), 201
    else:
        piis, parsed_content = process_string.process_string(raw_content)
        response = {
            "content": parsed_content.encode('ascii',errors='ignore'),
            "piis": piis,
        }
        return jsonify(response), 201

# Return error 404 in JSON format
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
