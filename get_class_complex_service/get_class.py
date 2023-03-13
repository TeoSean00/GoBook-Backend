import os
import requests
from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_cors import CORS
from os import environ


from datetime import datetime
import json

app = Flask(__name__)

CORS(app)  

@app.route('/', methods=('GET', 'POST'))
def index():
    return "Hello there, there are the classes"

# Getting classes signed up by user
@app.route('/users/getAttendedClasses/<userid>', methods=['GET'])
def get_class(userid):
    print("USER ID IS",userid)
    class_output = []
    user_data = requests.request("GET", "http://user_service:5001/users/" + userid)
    enrolled_classes = user_data.json()['attended_classes']
    for enrolled_class in enrolled_classes:
        class_data = requests.request("GET", "http://class_service:5000/class/" + enrolled_class)
        class_output.append(class_data.json())
    return class_output




# Booking class service can save for when we use it
@app.route('/users/joinclass/<userid>', methods=['PUT'])
# test userid 640c50c9ed0c22144794d080
# test classid 640c50c23203cab91d70d509
# REMEMBER TO CHANGE THE ID AND CLASS IN POSTMAN WHENEVER YOU DROP DATABASE
# Postman input data style for now: {"classId" : "640c50c23203cab91d70d509"}
def join_class(userid):
    data = request.get_json()
    class_data = data
    user_data = {
        "userId": userid,
    }
    classreq = requests.request("PUT", "http://localhost:5000/class/" + data['classId'], json = user_data)
    userreq = requests.request("PUT", "http://localhost:5001/users/addclass/" + userid, json = class_data)
    return data

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    app.run(host='0.0.0.0', port=5005, debug=True)