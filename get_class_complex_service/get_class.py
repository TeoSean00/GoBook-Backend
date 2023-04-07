import os
from flask import Flask, request
from flask_cors import CORS
from os import environ
from invokes import invoke_http

app = Flask(__name__)

PORT=5005
CORS(app)  

@app.route('/health', methods=('GET', 'POST'))
def index():
    return "get_class service is up and running"

# Complex microservice route to update class details, by invoking class service, user service and AMQP messaging service
@app.route('/update_class_details', methods=['PUT'])
def update_class():
    data = request.get_json()
    # * 1. Invoke class service to update class participant
    classID = data["metadata"]['classId']
    userID = data['metadata']['userID']
    runID = data['metadata']['runID']
    class_service_base_URL = environ.get('class_service_URL') or "http://localhost:5006"
    class_service_URL = class_service_base_URL + f"/{classID}/{runID}"
    userDataObject = {
        "userId": userID
    }
    classUpdateResult = invoke_http(class_service_URL, method = 'PUT', json = userDataObject)

    # * 2. Invoke user service to update user booking
    user_service_base_URL = environ.get('user_service_URL') or "http://localhost:5001"
    user_service_URL = user_service_base_URL + f"/addClass/{userID}"
    classDataObject = {
        "classId": classID
    }
    userUpdateResult = invoke_http(user_service_URL, method = 'PUT', json = classDataObject)

    # * 3. Sending msg thru AMQP to message service
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
        }, 500

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    app.run(host='0.0.0.0', port=PORT, debug=True)
print(f"get_class Service is initialized on port {PORT}")