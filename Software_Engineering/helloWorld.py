from flask import Flask, jsonify, abort, make_response
from flask import request
import time

## Note list
# users may re-upload their resumes. This generates a new job ID everytime they upload a new resume. 
# How do we link the job ID and the new resume with the same user? 
# Have a column 'user id' that contains each unique user id?

app = Flask(__name__)

# FOR TESTING PURPOSES - REMOVE THIS AFTER ESTABLISHING DATABASE
tasks = [
    {
        'job_id': 1,
        'operation': "scan",
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'job_id': 2,
        'operation': "purge",
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

# This function sends the uploaded resume to our scanning and masking functions 
# which will flag out PIIs and mask them inside the resume
# they will return both the flagged PIIs or masked contents back 
# after which, it will generate a job id and store the contents inside the database
# input: operation to be applied on Resume
# output: flagged PIIs, filtered contents, operation type, job id in JSON format
@app.route('/upload/<string:ops>', methods=['GET'])
def create_job(ops):
    # conn = db_connect.connect() # connect to database
    # query = conn.execute("select * from employees") # This line performs query and returns json result
    print(ops + "ing in progress...") # HOW TO DISPLAY INTERMIDIATE MESG IN TERMINAL?
    time.sleep(5)

    task = {
        'job_id': tasks[-1]['job_id'] + 1,
        'operation': ops,
        'PII': "A list of PIIs found using Scan function",
        'contents': {
            "contents": "A string of text after removing PIIs"
        }
    }
    tasks.append(task)
    return jsonify(task), 200

# This function gets the flagged PIIs and masked contents using the job id
# input: operation to be applied on Resume
# output: flagged PIIs, filtered contents, operation type, job id in JSON format
@app.route('/<int:job_id>', methods=['POST'])
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