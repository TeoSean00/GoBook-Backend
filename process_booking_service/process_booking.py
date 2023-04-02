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
# from kafka import KafkaProducer
import json
import pika
import requests
import amqp_setup
from invokes import invoke_http

app = Flask(__name__)

CORS(app)
portNum = 5008

update_booking_URL = "http://localhost:5007/update_booking"



# Setting up kafka producer for recommendation
# p = KafkaProducer(bootstrap_servers=['kafka:9092'],
#                          value_serializer=lambda x: json.dumps(x).encode('utf-8'))
# print("Kafka Producer has been initiated...")

# ! UI will call createpayment -> payment service creating payment intent
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

    response_data = requests.post(url, data=json.dumps(data), headers=headers)
    for item in response_data:
        print("ITEM IS", item)

    # data received is
    # {'amount': 1500, 'amount_capturable': 0, 'amount_details': {'tip': {}}, 'amount_received': 1500, 'automatic_payment_methods': {'enabled': True}, 'capture_method': 'automatic', 'client_secret': 'pi_3MnMh6JTqG9NvRuT0xGeHdCj_secret_gsKWOlAlwTsdvsj1Ru9cK6goW', 'confirmation_method': 'automatic', 'created': 1679234084, 'currency': 'sgd', 'id': 'pi_3MnMh6JTqG9NvRuT0xGeHdCj', 'latest_charge': {'id': 'ch_3MnMh6JTqG9NvRuT0DB1hg0w'}, 'livemode': False, 'metadata': {}, 'object': 'payment_intent', 'payment_method': {'id': 'pm_1MnMhFJTqG9NvRuT8Hf2rccH'}, 'payment_method_options': {'card': {'request_three_d_secure': 'automatic'}, 'paynow': {}}, 'payment_method_types': ['card', 'paynow'], 'status': 'succeeded'}
    response_str = response_data.content.decode()
    return json.loads(response_str)



#! Upon successful payment payment service will call this API with payment data
@app.route('/update_payment', methods=['POST'])
def process_booking():

    data = request.get_json()

    # this is to convert data to JSON string
    # dataObject = json.dumps(data)
    # print('This is error output', file=sys.stderr)
    print(data, file=sys.stderr)

    # Sample response data from payment service
    temporary_response_data = {'amount': 1420, 'amount_capturable': 0, 'amount_details': {'tip': {}}, 'amount_received': 1420, 'automatic_payment_methods': {'enabled': True}, 'capture_method': 'automatic', 'client_secret': 'pi_3MqawoJTqG9NvRuT1CIECYYH_secret_FhWhAZ6MUjAnfbAqvBOxOjxwB', 'confirmation_method': 'automatic', 'created': 1680003858, 'currency': 'sgd', 'id': 'pi_3MqawoJTqG9NvRuT1CIECYYH', 'latest_charge': {'id': 'ch_3MqawoJTqG9NvRuT1geYkf4z'}, 'livemode': False, 'metadata': {'courseDescription': "Define a coherent data strategy and spearhead new approaches to enrich, synthesise and apply data, to maximise the value of data as a critical business asset and driver.", 'userEmail': 'celov54484@gpipes.com', 'coursename': 'Advanced-Information-Management-Classroom-Asynchronous', 'runID': '1', 'orderID': '4500', 'userID': '112532673980137782859', 'classId': '642924c830f6877e418e1650'}, 'object': 'payment_intent', 'payment_method': {'id': 'pm_1Mqax8JTqG9NvRuTdQ8sxHYn'}, 'payment_method_options':
                               {'card': {'request_three_d_secure': 'automatic'}, 'paynow': {}}, 'payment_method_types': ['card', 'paynow'], 'status': 'succeeded'}


    # ? Now to update the class and user service that book is confirmed
    # ? 1. Invoke class service
    # ? 2. Invoke user service
    # ? 3. Invoke notification service to send email of ticket
    ##################################
    # Sending of booking data to kafka log
    # p.send('booking', data)
    ##################################

    # * 1. Invoke class service to update class participant
    classID = data['metadata']['classId']
    userID = data['metadata']['userID']
    runID = data['metadata']['runID']

    classServiceURL = "http://localhost:5006/class/{classID}/{runID}"
    classUpdateResult = invoke_http(classServiceURL, method = 'PUT')
    print("Class service update result code")
    print(classUpdateResult['code'])

    # * 2. Invoke user service to update user booking
    userServiceURL = "http://localhost:5001/user/addclass/{userID}"
    userDataObject = {
        "classID": classID,
    }
    userUpdateResult = invoke_http(userServiceURL, method = 'PUT', data = userDataObject)
    print("User service update result code")
    print(userUpdateResult['code'])

    # * 3. Sending msg thru AMQP to message service
    print('\n\n-----Backend updated, publishing the (class booking) message with routing_key=email.info-----')
    # notification is listening to email_service queue
    # binding key is email.info as well

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

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email.info",
        body=dataObject, properties=pika.BasicProperties(delivery_mode=2))

    return {
        "code": 201,
        "data": {
            "order": "booking of class is successful"
        }
    }

    # pass payment_response and class_booking jSON
    # class_booking will need to have class id , run id , userid
    # response = requests.request("POST", update_booking_URL,
    # json={
    #     "userEmail" : "keithloh99@gmail.com",
    #     "userName" : "Keith Loh",
    #     "orderID" : "4500",
    #     "courseName" : "Advanced-Information-Management-Classroom-Asynchronous",
    #     "coursePrice" : "1420",
    #     "courseDescription" : "Define a coherent data strategy and spearhead new approaches to enrich, synthesise and apply data, to maximise the value of data as a critical business asset and driver.",
    #     "classId" : 642924c830f6877e418e1650,
    #     "runId": 1,
    #     "userId": 112532673980137782859,
    #     }
    # )


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " to coordinate payments with updating of class and user services")
    app.run(host="0.0.0.0", port=portNum, debug=True)
print(f"Process Booking Service is initialized on port {portNum}")
