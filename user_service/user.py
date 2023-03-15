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

# For docker
# client = MongoClient(host='user_db',
#                         port=27018
#                         )
client = MongoClient(host='localhost',
                        port=27018
                        )

db = client['user_db']
sample_data = [
    {
    "name": "Test User 1",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
        "Review 2"
    ]
    },
    {
    "name": "Test User 2",
    "preferences": [],
    "attended_classes": [],
    "reviews": []
    },
    {
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
    "name": "Test User 4",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
    ]
    },
    {
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

# Creating users WILL DROP WHOLE DB PLEASE BEAR IN MIND
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
@app.route('/users/<userid>')
def get_user(userid):
    object = ObjectId(userid)
    myquery = { "_id": object }
    user = db.users.find_one(myquery)
    return json.loads(json_util.dumps(user))

# Add user but we dont need to
# @app.route('/users/<name>', methods=['POST'])
# def add_stored_animals(name):
#     addObject = {
#         "name": name,
#         "preferences": [],
#         "attended_classes": [],
#         "reviews": []
#         }
#     db.users.insert_one(addObject)
#     return addObject

# Update a user using his userid (Not sure if we should update by username instead ah)
# Test user 1 sample userid to use : 640b0cd4c65fe29244b71a53
# add review
@app.route('/users/addreview/<userid>', methods=['PUT'])
def add_review(userid):
    data = request.get_json() #This will be a the json put in the request. Use postman to add the review using PUT
    object = ObjectId(userid)
    myquery = { "_id": object }
    # myquery = db.users.find_one({"_id" : userid})
    newvalues = { "$push": { "reviews": data } }
    # query = db.users.find_one({"_id": object })
    updated_user = db.users.find_one_and_update(myquery, newvalues)
    return json.loads(json_util.dumps(updated_user))

# add class
@app.route('/users/addclass/<userid>', methods=['PUT'])
def add_class(userid):
    data = request.get_json() #This will be a the json put in the request. Use postman to add the review using PUT
    object = ObjectId(userid)
    myquery = { "_id": object }
    # myquery = db.users.find_one({"_id" : userid})
    newvalues = { "$push": { "attended_classes": data["classId"] } }
    # query = db.users.find_one({"_id": object })
    updated_user = db.users.find_one_and_update(myquery, newvalues)
    return json.loads(json_util.dumps(updated_user))

# Add preferences
@app.route('/users/addpref/<userid>', methods=['PUT'])
def add_preferences(userid):
    data = request.get_json() #This will be a the json put in the request. Use postman to add the review using PUT
    object = ObjectId(userid)
    myquery = { "_id": object }
    # myquery = db.users.find_one({"_id" : userid})
    newvalues = { "$push": { "preferences": data } }
    # query = db.users.find_one({"_id": object })
    updated_user = db.users.find_one_and_update(myquery, newvalues)
    return json.loads(json_util.dumps(updated_user))

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
