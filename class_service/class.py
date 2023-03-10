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

db = client['class_db']
sample_data = [
    {
    "className": "Data Breach Management (Synchronous e-learning)",
    "classSize": 10,
    "date": "10-4-2023",
    "participants": [
    ],
    "categories": ["PSEA","SF_Series"]
    },
    {
    "className": "Data Breach Management (Synchronous e-learning)",
    "classSize": 10,
    "date": "10-4-2023",
    "participants": [
    ],
    "categories": ["PSEA","SF_Series"]
    },
    {
    "className": "Data Breach Management (Synchronous e-learning)",
    "classSize": 10,
    "date": "10-4-2023",
    "participants": [
    ],
    "categories": ["PSEA","SF_Series"]
    },
    {
    "className": "Data Breach Management (Synchronous e-learning)",
    "classSize": 10,
    "date": "10-4-2023",
    "participants": [
    ],
    "categories": ["PSEA","SF_Series"]
    }
]


CORS(app)  

@app.route('/', methods=('GET', 'POST'))
def index():
    return "Hello there, there are the classes"


@app.route('/class')
def get_all_classes():
    classes = db.classes.find()
    return json.loads(json_util.dumps(classes))


@app.route('/class/createDB')
def create_db():
    db_exists = client.list_database_names()
    if 'class_db' in db_exists:
        client.drop_database('class_db')
    db = client['class_db']
    for data in sample_data:
        db["classes"].insert_one(data)
    return "Sample data inserted successfully" + str(sample_data)



if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
