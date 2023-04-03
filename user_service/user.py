import os
from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_cors import CORS
from os import environ
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
import json


app = Flask(__name__)
portNum = 5001
# For docker
client = MongoClient(host='user_db',
                        port=27018
                        )
# client = MongoClient(host='localhost',
#                         port=27018
#                         )

db = client['user_db']
sample_data = [
    {
    "userId": "112532673980137782859",
    "given_name": "Keith Loh",
    "email" : "keith.loh.2021@scis.smu.edu.sg",
    "name": "Test User 1",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
        "Review 2"
    ]
    },
    {
    "userId": "113532673980137782859",
    "given_name": "Joseph Hee",
    "email" : "joseph.hee.2021@scis.smu.edu.sg",
    "name": "Test User 2",
    "preferences": [],
    "attended_classes": [],
    "reviews": []
    },
    {
    "userId": "114532673980137782859",
    "given_name": "Tyler Lian",
    "email" : "tyler.lian.2021@scis.smu.edu.sg",
    "name": "Test User 3",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
        "Review 2",
        "Review 3"
    ]
    },
    {
    "userId": "115542673980137782859",
    "given_name": "Keith Lee",
    "email" : "keithloh99@gmail.com",
    "name": "Test User 4",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
    ]
    },
    {
    "userId": "116532673980137782859",
    "given_name": "Elton Tay",
    "email" : "elton.tay.2021@scis.smu.edu.sg",
    "name": "Test User 5",
    "preferences": [],
    "attended_classes": [],
    "reviews": []
    },
]

CORS(app)  

@app.route('/', methods=('GET', 'POST'))
def index():
    return "Hello there, there are the users"

# Initalise the database with sample data
@app.route('/users/createDB')
def create_db():
    db_exists = client.list_database_names()
    if 'user_db' in db_exists:
        client.drop_database('user_db')
    db = client['user_db']
    for data in sample_data:
        db["users"].insert_one(data)
    return "Sample data inserted successfully" + str(sample_data)

# find all users
@app.route('/users')
def get_all_users():
    users = db.users.find()
    return json.loads(json_util.dumps(users))

# Get one user by their id (Or can change to name)
@app.route('/users/<userId>')
def get_user(userId):
    # ! not needed anymore as we arent using objectid
    # object = ObjectId(userid)
    myquery = { "userId": userId }
    user = db.users.find_one(myquery)
    return json.loads(json_util.dumps(user))

# Add user but we dont need to
@app.route('/users/adduser', methods=['POST'])
def add_stored_animals():
    data = request.get_json()
    # ? Sample User JSON object
    #{
    # "userid": "112532673980137782859",
    # "given_name": "Keith Loh",
    # "email" : "keith.loh.2021@scis.smu.edu.sg",
    # "name": "Test User 1"
    # }

    addObject = {
        "userid": data["userid"],
        "given_name": data["given_name"],
        "email" : data["email"],
        "name": data["name"],
        "preferences": [],
        "attended_classes": [],
        "reviews": []
        }
    db.users.insert_one(addObject)
    return addObject

# Update a user using his userid (Not sure if we should update by username instead ah)
# Test user 1 sample userid to use : 640b0cd4c65fe29244b71a53
# ? subjected to changes - keith
# add review
@app.route('/users/addreview/<userId>', methods=['PUT'])
def add_review(userId):
    data = request.get_json() #This will be a the json put in the request. Use postman to add the review using PUT
    data = json.loads(data)
    myquery = { "userId": userId }
    # myquery = db.users.find_one({"_id" : userid})
    newvalues = { "$push": { "reviews": data } }
    # query = db.users.find_one({"_id": object })
    updated_user = db.users.find_one_and_update(myquery, newvalues)
    return json.loads(json_util.dumps(updated_user))

# add class attended to userID
@app.route('/users/addclass/<userId>', methods=['PUT'])
def add_class(userId):
    data = request.get_json() #This will be a the json put in the request. Use postman to add the review using PUT
    data = json.loads(data)
    myquery = { "userId": userId }
    # myquery = db.users.find_one({"_id" : userid})
    newvalues = { "$push": { "attended_classes": data["classId"] } }
    # query = db.users.find_one({"_id": object })
    updated_user = db.users.find_one_and_update(myquery, newvalues)
    print("UPDATED USER IS ", updated_user)
    # ! doesn't show the updated user (pls fix)
    return json.loads(json_util.dumps(updated_user))



# Add preferences
@app.route('/users/addpref/<userId>', methods=['PUT'])
def add_preferences(userId):
    data = request.get_json() #This will be a the json put in the request. Use postman to add the review using PUT
    data = json.loads(data)
    myquery = { "userId": userId }
    # myquery = db.users.find_one({"_id" : userid})
    newvalues = { "$push": { "preferences": data['preference'] } }
    # query = db.users.find_one({"_id": object })
    updated_user = db.users.find_one_and_update(myquery, newvalues)
    return json.loads(json_util.dumps(updated_user))



if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    app.run(host='0.0.0.0', port=portNum, debug=True)
print(f"User Service is initialized on port {portNum}")