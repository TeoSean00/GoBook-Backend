import os
import sys
import requests
from flask import Flask, Response, render_template, request, url_for, redirect, jsonify
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
import amqp_setup
from invokes import invoke_http

app = Flask(__name__)

PORT = 5008
CORS(app)


# Setting up kafka producer for recommendation
p = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))
print("Kafka Producer has been initiated...")

@app.route('/health', methods=['GET'])
def health():
    return "Process booking service is running and healthy"

# ! UI will call createpayment -> payment service creating payment intent
@app.route('/booking/createPayment', methods=['POST'])
@cross_origin()
def create_payment():
    data = request.get_json()
    print('This is file recevied by create_payment', file=sys.stderr)
    print(data, file=sys.stderr)
    # This is for docker
    # url = environ.get('payment_service_URL') or 'http://localhost:8080/create-payment-intent'
    url = 'http://host.docker.internal:8080/create-payment-intent'
    # url = 'http://localhost:8080/create-payment-intent'
    headers = {'Content-Type': 'application/json'}

    response_data = requests.post(url, data=json.dumps(data), headers=headers)
    for item in response_data:
        print("ITEM IS", item, file=sys.stderr)
    response_str = response_data.content.decode()
    return json.loads(response_str), 200

#! Upon successful payment payment service will call this API with payment data
@app.route('/update_payment', methods=['POST'])
@cross_origin()
def process_booking():
    data = request.get_json()
    print(data, file=sys.stderr)

    # this is to convert data to JSON string
    # dataObject = json.dumps(data)
    # print('This is error output', file=sys.stderr)
    print("DATA RESPONSE IS HERE",data,file=sys.stderr)
    print("DATA IS HERE", file=sys.stderr)
    print(data, file=sys.stderr)

    # Sample response data from payment service
    {
    "amount": 1420,
    "amount_capturable": 0,
    "amount_details": {
        "tip": {}
    },
    "amount_received": 1420,
    "automatic_payment_methods": {
        "enabled": True
    },
    "capture_method": "automatic",
    "client_secret": "pi_3MqawoJTqG9NvRuT1CIECYYH_secret_FhWhAZ6MUjAnfbAqvBOxOjxwB",
    "confirmation_method": "automatic",
    "created": 1680003858,
    "currency": "sgd",
    "id": "pi_3MqawoJTqG9NvRuT1CIECYYH",
    "latest_charge": {
        "id": "ch_3MqawoJTqG9NvRuT1geYkf4z"
    },
    "livemode": False,
    "metadata": {
        "courseDescription": "Define a coherent data strategy and spearhead new approaches to enrich, synthesise and apply data, to maximise the value of data as a critical business asset and driver.",
        "userEmail": "celov54484@gpipes.com",
        "coursename": "Advanced-Information-Management-Classroom-Asynchronous",
        "runID": "1",
        "orderID": "4500",
        "userID": "112532673980137782859",
        "classId": "64294fd360d77b957414d18b"
    },
    "object": "payment_intent",
    "payment_method": {
        "id": "pm_1Mqax8JTqG9NvRuTdQ8sxHYn"
    },
    "payment_method_options": {
        "card": {
            "request_three_d_secure": "automatic"
        },
        "paynow": {}
    },
    "payment_method_types": [
        "card",
        "paynow"
    ],
    "status": "succeeded"
}
    
    # ? Now to update the class and user service that book is confirmed

    # ? 1. Call get_class complex to Invoke class service and user service
    # ? 2. Invoke notification service to send email of ticket

    ##################################
    # Sending of booking data to kafka log
    ##################################
    print("META DATA RECEIVED IS",data["metadata"],file=sys.stderr)
    p.send('booking', data)

    # * 1. Invoke get_class service to update class participant and update user attended classes
    get_classes_base_URL = environ.get('get_classes_base_URL') or "http://localhost:5005"
    get_classes_URL = get_classes_base_URL + f"/update_class_details"
    get_classes_updateResult = invoke_http(get_classes_URL, method = 'PUT', json = data)

    # * 2. Sending msg thru AMQP to message service
    print('\n\n-----Backend updated, publishing the (class booking) message with routing_key=email.info-----',file=sys.stderr)
    # notification is listening to email_service queue
    # binding key is email.info as well
    classID = data['metadata']['classId']
    userID = data['metadata']['userID']
    runID = data['metadata']['runID']

    dataObject = {
        "userEmail" : data['metadata']['userEmail'],
        "userName" : data['metadata']['userEmail'],
        "orderID" : data['metadata']['orderID'],
        "courseName" : data['metadata']['coursename'],
        "coursePrice" : data['amount'],
        "courseDescription" : data['metadata']['courseDescription'],
        "classID" : classID,
        "runID" : runID,
        "userID" : userID
    }
    print("get_classes_updateResult is", get_classes_updateResult,file=sys.stderr)
    print("get_classes_updateResult is", get_classes_updateResult,file=sys.stderr)

    # if (classUpdateResult['code'] in range(200,300) and userUpdateResult['code'] in range(200,300)):
    if (get_classes_updateResult['code'] in range(200,300)):
        dataObject = json.dumps(dataObject)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email.info",
            body=dataObject, properties=pika.BasicProperties(delivery_mode=2))

        return {
            "code": 200,
            "userUpdate": get_classes_updateResult["userUpdate"],
            "classUpdate": get_classes_updateResult["classUpdate"],
            "email": "sent to queue successfullyx"
        },200
    else:
        return {
            "code": 500,
            "userUpdate": get_classes_updateResult["userUpdate"],
            "classUpdate": get_classes_updateResult["classUpdate"],
            "email": "did not send to queue"
        },500

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " to coordinate payments with updating of class and user services")
    app.run(host="0.0.0.0", port=PORT, debug=True)
print(f"Process Booking Service is initialized on port {PORT}")
