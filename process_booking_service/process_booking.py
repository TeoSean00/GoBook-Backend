import os
import sys
import requests
from flask import Flask, Response,render_template, request, url_for, redirect,jsonify
from flask_cors import CORS, cross_origin
from os import environ
# from pymongo import MongoClient
# from bson import json_util
# from bson.objectid import ObjectId

from datetime import datetime
import json

app = Flask(__name__)

CORS(app)  

update_booking_URL = "http://localhost:5007/update_booking"

# Mongo Client
# client = MongoClient(host='localhost',
#                         port=27017
#                         )
# 
@app.route('/update_payment', methods=['POST'])
def process_booking():
    # pass payment_response and class_booking jSON
    # class_booking will need to have class id , run id , userid
    response = requests.request("POST", update_booking_URL,
    # json=payment response and class data
    )
    return 


@app.route('/booking/createPayment', methods=['POST'])
@cross_origin()
def create_payment():
    data = request.get_json()
    class_output = []
    # This is for docker
    # user_data = requests.request("GET", "http://user_service:5001/users/" + userid)
    url = 'http://localhost:8080/create-payment-intent'
    response_data = requests.post(url,data)
    for item in response_data:
        print("ITEM IS",item)
    
    response_str = response_data.content.decode()
    return json.loads(response_str)


"""
Order JSON Object parsed into ProcessEmailService should follow this format
{
userEmail: String,
userName: String,
orderID: String,
courseName: String,
coursePrice: String,
courseDescription: String
}

Example of Order JSON Object
{
    "userEmail" : "celov54484@gpipes.com",
    "userName" : "celo",
    "orderID" : "4500",
    "courseName" : "Data Structure Algorithms",
    "coursePrice" : "$2000",
    "courseDescription" : "A 3rd semester course at SMU, continues to develop students' understanding of object oriented programming, memory management"
    "classID" : 3,
    "runID": 1,
    "userID": 10,
}
"""



if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " to register for a class")
    app.run(host="0.0.0.0", port=5008, debug=True)
print(f"Flask app is initialized on port 5007")