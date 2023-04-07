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

PORT = 5004
DB_ENVIRONMENT = environ.get('DB_ENVIRONMENT') or "localhost"
client = MongoClient(host=DB_ENVIRONMENT,
                        port=27021
                    )

db = client['review_db']
sample_data = [
    {
    "userId":"116532673980137782859",
    "classId":"2",
    "date":"12-2-2023",
    "rating": 1,
    "reviewContent": "Poor Lesson",
    },
    {
    "userId":"115542673980137782859",
    "classId":"2",
    "date":"10-3-2023",
    "rating": 5,
    "reviewContent": "Good Lesson",
    },
    {
    "userId":"114532673980137782859",
    "classId":"1",
    "date":"8-1-2023",
    "rating": 3,
    "reviewContent": "Still ok la this instructor, might not go again",
    },
]

CORS(app)  

@app.route('/health', methods=['GET'])
def index():
    return "Review service is running and healthy"


@app.route('/' , methods=['GET'])
def get_all_classes():
    reviews = db.reviews.find()
    return json.loads(json_util.dumps(reviews))
# initialise reviews_DB with the one above
@app.route('/createDB')
def create_db():
    db_exists = client.list_database_names()
    if 'review_db' in db_exists:
        client.drop_database('review_db')
    db = client['review_db']
    for data in sample_data:
        db["reviews"].insert_one(data)
    return "Sample data inserted successfully" + str(sample_data)

# get all reviews made by user
@app.route('/user/<userId>')
def get_classes_from_user(userId):
    reviews  = db.reviews.find( { "userId": userId } )
    return json.loads(json_util.dumps(reviews))

# get all reviews fors this class
@app.route('/class/<classId>')
def get_reviews_for_class(classId):
    reviews = db.reviews.find({"classId": classId})
    return json.loads(json_util.dumps(reviews))

# add review
@app.route('/', methods=['POST'])
def add_user_review():
    data = request.get_json() #This will be a the json put in the request. Use postman to add the partcipant using PUT
    db.reviews.insert_one(data)
    return "added review successfully"

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage class Schedule ...")
    create_db()
    app.run(host='0.0.0.0', port=PORT, debug=True)
print(f"Review Service is initialized on port {PORT}")