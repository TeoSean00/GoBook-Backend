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
from kafka import KafkaProducer
import json
import pika
import requests

app = Flask(__name__)

CORS(app)  

update_booking_URL = "http://localhost:5007/update_booking"

p = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))
print("Kafka Producer has been initiated...")

@app.route('/update_payment', methods=['POST'])
def process_booking():

    data = request.get_json()
    print('This is error output', file=sys.stderr)
    print(data, file=sys.stderr)

    url = 'http://host.docker.internal:5007/update_booking'
    headers = {'Content-Type': 'application/json'}
    response_data = requests.post(url,data=json.dumps(data),headers=headers)

    # send data to the kafka log
    p.send('booking', data)
    
    # pass payment_response and class_booking jSON
    # class_booking will need to have class id , run id , userid
    response = requests.request("POST", update_booking_URL,
    # for testing
    json={
        "userEmail" : "celov54484@gpipes.com",
        "userName" : "celo",
        "orderID" : "4500",
        "courseName" : "Data Structure Algorithms",
        "coursePrice" : "$2000",
        "courseDescription" : "A 3rd semester course at SMU, continues to develop students' understanding of object oriented programming, memory management",
        "classId" : 3,
        "runId": 1,
        "userId": 10,
        }
    )

    return {
        "code": 201,
        "data": {
            "order": "success"
        }
    }

@app.route('/booking/createPayment', methods=['POST'])
@cross_origin()
def create_payment():
    data = request.get_json()
    print('This is file recevied by create_payment', file=sys.stderr)
    print(data, file=sys.stderr)
    # This is for docker
    url = 'http://host.docker.internal:8080/create-payment-intent'
    # url = 'http://localhost:8080/create-payment-intent'
    headers = {'Content-Type': 'application/json'}

    response_data = requests.post(url,data=json.dumps(data),headers=headers)
    for item in response_data:
        print("ITEM IS",item)

    # data received is 
    # {'amount': 1500, 'amount_capturable': 0, 'amount_details': {'tip': {}}, 'amount_received': 1500, 'automatic_payment_methods': {'enabled': True}, 'capture_method': 'automatic', 'client_secret': 'pi_3MnMh6JTqG9NvRuT0xGeHdCj_secret_gsKWOlAlwTsdvsj1Ru9cK6goW', 'confirmation_method': 'automatic', 'created': 1679234084, 'currency': 'sgd', 'id': 'pi_3MnMh6JTqG9NvRuT0xGeHdCj', 'latest_charge': {'id': 'ch_3MnMh6JTqG9NvRuT0DB1hg0w'}, 'livemode': False, 'metadata': {}, 'object': 'payment_intent', 'payment_method': {'id': 'pm_1MnMhFJTqG9NvRuT8Hf2rccH'}, 'payment_method_options': {'card': {'request_three_d_secure': 'automatic'}, 'paynow': {}}, 'payment_method_types': ['card', 'paynow'], 'status': 'succeeded'}  
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
    print("This is flask " + os.path.basename(__file__) + " to coordinate payments with updating of class and user services")
    app.run(host="0.0.0.0", port=5008, debug=True)
print(f"Flask app is initialized on port 5007")