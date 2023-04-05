import os
from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_cors import CORS
from os import environ
from pymongo import MongoClient
from pymongo import ReturnDocument
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
import json


app = Flask(__name__)
portNum = 5001
# Switches between DB_ENVIRONMENT and localhost depending on whether the app is running on docker or not
DB_ENVIRONMENT = environ.get('DB_ENVIRONMENT') or "localhost"
client = MongoClient(host=DB_ENVIRONMENT,
                        port=27018
                    )

CORS(app) 


db = client['user_db']
sample_data = [
    {
    "_id": "112532673980137782859",
    "given_name": "Keith Loh",
    "email" : "keith.loh.2021@scis.smu.edu.sg",
    "picture": "",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
        "Review 2"
    ],
    "recommended_classes": [],
    },
    {
    "_id": "113532673980137782859",
    "given_name": "Joseph Hee",
    "email" : "joseph.hee.2021@scis.smu.edu.sg",
    "picture": "",
    "preferences": [],
    "attended_classes": [],
    "reviews": [],
    "recommended_classes": [],
    },
    {
    "_id": "114532673980137782859",
    "given_name": "Tyler Lian",
    "email" : "tyler.lian.2021@scis.smu.edu.sg",
    "picture": "",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
        "Review 2",
        "Review 3"
    ],
    "recommended_classes": [],
    },
    {
    "_id": "115542673980137782859",
    "given_name": "Teo Sean",
    "email" : "teosean@outlook.com",
    "picture": "",
    "preferences": [],
    "attended_classes": [],
    "reviews": [
        "Review 1",
    ],
    "recommended_classes": [],
    },
    {
    "_id": "116532673980137782859",
    "given_name": "Elton Tay",
    "email" : "elton.tay.2021@scis.smu.edu.sg",
    "picture": "",
    "preferences": [],
    "attended_classes": [],
    "reviews": [],
    "recommended_classes": [],
    },
] 

def main():
    print("Loading in user data...")
    db_exists = client.list_database_names()
    if 'user_db' in db_exists:
        client.drop_database('user_db')
    db = client['user_db']
    for data in sample_data:
        db["users"].insert_one(data)
    return "Sample data inserted successfully" + str(sample_data)

# <-------------------------------------------Routes for userDB------------------------------------------->
@app.route('/', methods=('GET', 'POST'))
def index():
    return "Hello there, there are the users"

# Initalise the user database with the sample data above
@app.route('/users/createDB')
def create_db():
    db_exists = client.list_database_names()
    if 'user_db' in db_exists:
        client.drop_database('user_db')
    db = client['user_db']
    for data in sample_data:
        db["users"].insert_one(data)
    return "Sample data inserted successfully" + str(sample_data)

# Get all users in the userDB
@app.route('/users/getUsers')
def get_all_users():
    users = db.users.find()
    if (users == None):
        return "no users in DB"
    else:
        return json.loads(json_util.dumps(users))

# Get a particular user by their userId else return string saying no such user
@app.route('/users/getUser/<userId>')
def get_user(userId):
    myquery = { "_id": userId }
    user = db.users.find_one(myquery)
    if user == None:
        return "no such user"
    return json.loads(json_util.dumps(user))

# Add user to the userDB if user does not exist in DB, else return string saying user exists already
@app.route('/users/addUser', methods=['POST'])
def add_user():
    data = request.get_json()
    if (data == None):
        return "invalid user details"
    else:
        addObject = {            
            "_id": data["id"],
            "given_name": data["given_name"],
            "email": data["email"],
            "picture": data["picture"],
            "preferences": [],
            "attended_classes": [],
            "recommended_classes": [],
        }
        db.users.insert_one(addObject)
        return addObject

# Update a user using his userid
# Test user 1 sample userid to use : 640b0cd4c65fe29244b71a53
# ? subjected to changes - keith
# add review
# @app.route('/users/addreview/<userId>', methods=['PUT'])
# def add_review(userId):
#     data = request.get_json() #This will be a the json put in the request. Use postman to add the review using PUT
#     data = json.loads(data)
#     myquery = { "_id": userId }
#     # myquery = db.users.find_one({"_id" : userid})
#     newvalues = { "$push": { "reviews": data } }
#     # query = db.users.find_one({"_id": object })
#     updated_user = db.users.find_one_and_update(myquery, newvalues, return_document = ReturnDocument.AFTER)
#     return json.loads(json_util.dumps(updated_user))

# add class attended to userID
@app.route('/users/addclass/<userId>', methods=['PUT'])
def add_class(userId):
    data = request.get_json() #This will be a the json put in the request. Use postman to add the class using PUT
    data = json.loads(data)
    myquery = { "_id": userId }
    # myquery = db.users.find_one({"_id" : userid})
    newvalues = { "$push": { "attended_classes": data["classId"] } }
    # query = db.users.find_one({"_id": object })
    updated_user = db.users.find_one_and_update(myquery, newvalues)
    return json.loads(json_util.dumps(updated_user))

# Add preferences
@app.route('/users/addpref/<userId>', methods=['PUT'])
def add_preferences(userId):
    data = request.get_json() #This will be a the json put in the request. Use postman to add the preferences using PUT
    # data = json.loads(data)
    myquery = { "_id": userId }
    # myquery = db.users.find_one({"_id" : userid})
    newvalues = { "$push": { "preferences": data['preference'] } }
    # query = db.users.find_one({"_id": object })
    # try :
    #     updated_user = db.users.find_one_and_update(myquery, newvalues, returnDocument = ReturnDocument.AFTER)
    # except :
    #     return "error"
    updated_user = db.users.find_one_and_update(myquery, newvalues)
    return json.loads(json_util.dumps(updated_user))

# Add recommended classes
@app.route('/users/addrecc/<userId>', methods=['PUT'])
def add_recommendations(userId):
    data = request.get_json() #This will be a the json put in the request. Use postman to add the recommendationsD using PUT
    # data = json.loads(data)
    myquery = { "_id": userId }
    # myquery = db.users.find_one({"_id" : userid})
    newvalues = { "$set": { "recommended_classes": data['recommended_classes'] } }
    # query = db.users.find_one({"_id": object })
    # try :
    #     updated_user = db.users.find_one_and_update(myquery, newvalues, returnDocument = ReturnDocument.AFTER)
    # except :
    #     return "error"
    updated_user = db.users.find_one_and_update(myquery, newvalues)
    return json.loads(json_util.dumps(updated_user))

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    main()
    app.run(host='0.0.0.0', port=portNum, debug=True)
print(f"User Service is initialized on port {portNum}")