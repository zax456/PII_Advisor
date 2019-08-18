### NOT IN USE YET ###
from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Resource, Api
import time
 
app = Flask(__name__)
api = Api(app)

 ### TODO ###
 # Turn into RESTful API
class User_file_upload(Resource):
    # function first send uploaded document to have PIIs flagged out and returned 
    # afterwhich, it sends the document and flagged PIIs to have them removed from document 
    # return cleaned contents as JSON
    def post(self, doc):
        # send doc to flag out PIIs (during user file upload)

        # put JSON in database
        new_upload = {
            'operation': "",
            'PII': "A list of PIIs found using Scan function",
            'contents': {
                "contents": "A string of text after removing PIIs"
                }
            }
        return {
            'document': new_upload,
            'result': "Successfully masked PIIs in document!"
            }, 201

# Retrieve document with its flagged PIIs and masked contents from database
class Results(Resource):
    def get(self, job_id):
        return ''

### Add Resources (routes) here ###
api.add_resource(User_file_upload, '/upload') # when user uploads resume
api.add_resource(Results, '/result/<string:job_id>') # when user uploads resume

if __name__ == '__main__':
    app.run(debug=True)