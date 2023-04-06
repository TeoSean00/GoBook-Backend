import os
import requests
from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_cors import CORS
from os import environ
from invokes import invoke_http

from datetime import datetime
import json

app = Flask(__name__)

PORT=5005
CORS(app)  

@app.route('/health', methods=('GET', 'POST'))
def index():
    return "get_class service is up and running"

# Getting classes signed up by user
@app.route('/<userid>', methods=['GET'])
def get_class(userid):
    print("USER ID IS",userid)
    class_output = []
    user_service_url = environ.get('user_service_URL') or "http://localhost:5001"
    class_service_url = environ.get('class_serice_URL') or "http://localhost:5006"
    user_data = requests.request("GET", user_service_url + "/" + userid)
    enrolled_classes = user_data.json()['attended_classes']
    for enrolled_class in enrolled_classes:
        # This is for docker
        # class_data = requests.request("GET", "http://class_service:5006/class/" + enrolled_class)
        class_data = requests.request("GET", class_service_url + "/" + str(enrolled_class))
        class_output.append(class_data.json())
    return class_output

@app.route('/update_class_details', methods=['PUT'])
def update_class():
    data = request.get_json()
    # * 1. Invoke class service to update class participant
    print("Starting slicing of json data")
    classID = data["metadata"]['classId']
    userID = data['metadata']['userID']
    runID = data['metadata']['runID']
    class_service_base_URL = environ.get('class_service_URL') or "http://localhost:5006"
    class_service_URL = class_service_base_URL + f"/{classID}/{runID}"
    # f"http://localhost:5006/class/{classID}/{runID}" or environ('class_service_URL')
    userDataObject = {
        "userId": userID
    }
    #? JSONIFY the data object
    userDataObject = json.dumps(userDataObject)

    # userDataObject = jsonify(userDataObject)
    classUpdateResult = invoke_http(class_service_URL, method = 'PUT', json = userDataObject)

    print("Class service update result code")
    print(f"Class service URL is {class_service_URL}")
    print(userDataObject)
    print(classUpdateResult)
    print(type(classUpdateResult))

    # * 2. Invoke user service to update user booking
    user_service_base_URL = environ.get('user_service_URL') or "http://localhost:5001"
    user_service_URL = user_service_base_URL + f"/addClass/{userID}"
    classDataObject = {
        "classId": classID
    }
    #? JSONIFY the data object
    classDataObject = json.dumps(classDataObject)
    # classDataObject = jsonify(classDataObject)

    userUpdateResult = invoke_http(user_service_URL, method = 'PUT', json = classDataObject)
    print("User service update result code")
    print(f"User service URL is {user_service_URL}")
    print(classDataObject)
    print(userUpdateResult)
    print(type(userUpdateResult))

    # * 3. Sending msg thru AMQP to message service
    print('\n\n-----Class_ updated, return success to process_booking-----')
    # notification is listening to email_service queue
    # binding key is email.info as well
    if (userUpdateResult and classUpdateResult):
        return {
            "code": 200,
            "userUpdate": userUpdateResult,
            "classUpdate": classUpdateResult,
        }
    else:
        return {
            "code": 500,
            "userUpdate": userUpdateResult,
            "classUpdate": classUpdateResult,
            "email": "did not send to queue"
        }


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
print(f"get_class Service is initialized on port {PORT}")