from flask import Flask, request, jsonify, abort, make_response
import time

# TEST COMMANDS
# curl POST -d "piis=['Male', '22']&raw_contents=Ang Kian Hwee is the greatest!" 192.168.99.100:5000/upload/

## Note list
# users may re-upload their resumes. This generates a new job ID everytime they upload a new resume. 
# How do we link the job ID and the new resume with the same user? 
# Have a column 'user id' that contains each unique user id?

app = Flask(__name__)

# FOR TESTING PURPOSES - REMOVE THIS AFTER ESTABLISHING DATABASE
tasks = [
    {
        'job_id': 1,
        'operation': {
            'Scan': {
                'PII': ['Male', 'S1234567A', 'abc@gmail.com', 'PES F']
                }, 
            'Purge': {
                'Contents': "Peter Tay, MSe in Electrical Engineering"
                }
            }
    },
    {
        'job_id': 2,
        'operation': {
            'Scan': {
                'PII': ['Female', 'S1234568B', 'Maid', '23'] 
                }, 
            'Purge': {
                'Contents': "Mary Tan, BSc in Data Analytics"
                }
            }
    }
]

# This function sends the uploaded resume to our scanning and masking functions 
# which will flag out PIIs and mask them inside the resume
# they will return both the flagged PIIs or masked contents back 
# after which, it will generate a job id and store the contents inside the database
# input: operation to be applied on Resume
# output: flagged PIIs, filtered contents, operation type, job id in JSON format
@app.route('/upload/', methods=['POST'])
def read_resume():
    # conn = db_connect.connect() # connect to database
    # query = conn.execute("select * from employees") # This line performs query and returns json result

    ## Process the raw contents of the document - flagging, masking
    # remove this line after discussion on how to read raw document
    processed_text = process_text({'piis': request.form.get('piis'), 
                                   'raw_contents': request.form.get('raw_contents')}) 
    piis = processed_text['PIIs']
    parsed_contents = processed_text['Parsed contents']

    task = {
        'job_id': tasks[-1]['job_id'] + 1,
        'operation': {
            'Scan': {
                'PII': piis
                }, 
            'Purge': {
                'Contents': parsed_contents
                }
            }
    }
    tasks.append(task)
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

# This function gets the flagged PIIs and masked contents using the job id
# input: operation to be applied on Resume
# output: flagged PIIs, filtered contents, operation type, job id in JSON format
@app.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    task = [task for task in tasks if task['job_id'] == job_id]
    if len(task) == 0:
        abort(404)

    return jsonify(task[0])

# Return error 404 in JSON format
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)