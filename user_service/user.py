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


client = MongoClient(host='localhost',
                        port=27017
                        )

db = client['user_db']
    

CORS(app)  

@app.route('/', methods=('GET', 'POST'))
def index():
    return "Hello there, there are the users"

@app.route('/users')
def get_stored_animals():
    users = db.users.find()
    print(users)
    return json.loads(json_util.dumps(users))


# @app.route('/users/add', methods=['GET'])
# def add_stored_animals():
#     addObject = {
#         "name": "Test User 5",
#         "preferences": [],
#         "attended_classes": [],
#         "reviews": []
#         }
#     db.users.insert_one(addObject)
#     return addObject

@app.route('/users/<userid>', methods=['PUT'])
def update_stored_animals(userid):
    object = ObjectId(userid)
    myquery = { "_id": object }
    # myquery = db.users.find_one({"_id" : userid})
    newvalues = { "$set": { "reviews": ["Review 1", "Review 2", "Review 3"] } }
    # query = db.users.find_one({"_id": object })
    db.users.find_one_and_update(myquery, newvalues)
    return "USER ID RETURNED IS " + str(userid)

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
