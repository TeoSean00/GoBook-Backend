import os
from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_cors import CORS
from os import environ
from pymongo import MongoClient
from bson import json_util

from datetime import datetime
import json

app = Flask(__name__)


client = MongoClient(host='localhost',
                        port=27017
                        )

db = client['class_schedule']
    

CORS(app)  

@app.route('/', methods=('GET', 'POST'))
def index():
    return "Hello there, there are the classes"

@app.route('/users')
def get_stored_animals():
    _users = db.users.find()
    print(_users)
    users = [{"id": user["_id"], "name": user["username"]} for user in _users]
    print(users)
    return json.loads(json_util.dumps(users))

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
