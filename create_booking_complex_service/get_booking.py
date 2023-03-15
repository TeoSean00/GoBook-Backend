import os

from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_cors import CORS
from os import environ
# from pymongo import MongoClient
# from bson import json_util
# from bson.objectid import ObjectId

from datetime import datetime
import json
import pika

import amqp_setup

app = Flask(__name__)

CORS(app)  

# Mongo Client
# client = MongoClient(host='localhost',
#                         port=27017
#                         )
# 




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

{
    "userEmail" : "celov54484@gpipes.com",
    "userName" : "celo",
    "orderID" : "4500",
    "courseName" : "Data Structure Algorithms",
    "coursePrice" : "$2000",
    "courseDescription" : "A 3rd semester course at SMU, continues to develop students' understanding of object oriented programming, memory management"
}

"""


# Route to test if this complex microservice, using AMQP can call message_service
@app.route("/emailservice", methods=['POST'])
def processEmailService():

    # order = request.json.get()
    order = request.get_json()
    # print(order)
    order_msg = json.dumps(order)
    print("order msg is after this")
    print(order_msg)
    # Send the order object to the messaging microservice
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="message.", 
            body=order_msg, properties=pika.BasicProperties(delivery_mode = 2))
    
    # Test Return statement
    return {
        "code": 201,
        "data": {
            "order": "success"
        }
    }


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " to register for a class")
    app.run(host="0.0.0.0", port=5007, debug=True)
print(f"Flask app is initialized on port 5007")