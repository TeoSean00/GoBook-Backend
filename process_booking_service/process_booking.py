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

CORS(app)


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
    dataObject = json.dumps(data)
    # print('This is error output', file=sys.stderr)
    print(data, file=sys.stderr)

    # Sample response data from payment service
    temporary_response_data = {'amount': 200000, 'amount_capturable': 0, 'amount_details': {'tip': {}}, 'amount_received': 200000, 'automatic_payment_methods': {'enabled': True}, 'capture_method': 'automatic', 'client_secret': 'pi_3MqawoJTqG9NvRuT1CIECYYH_secret_FhWhAZ6MUjAnfbAqvBOxOjxwB', 'confirmation_method': 'automatic', 'created': 1680003858, 'currency': 'sgd', 'id': 'pi_3MqawoJTqG9NvRuT1CIECYYH', 'latest_charge': {'id': 'ch_3MqawoJTqG9NvRuT1geYkf4z'}, 'livemode': False, 'metadata': {'courseDescription': "A 3rd semester course at SMU, continues to develop students' understanding of object oriented programming, memory management", 'userEmail': 'celov54484@gpipes.com', 'coursename': 'Data Structure Algorithms', 'runID': '1', 'orderID': '4500', 'userID': '10', 'classId': '3'}, 'object': 'payment_intent', 'payment_method': {'id': 'pm_1Mqax8JTqG9NvRuTdQ8sxHYn'}, 'payment_method_options':
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
    classID = dataObject['metadata']['classId']
    userID = dataObject['metadata']['userID']
    runID = dataObject['metadata']['runID']

    classServiceURL = "http://localhost:5006/class/{classID}/{userID}/{runID}"
    classUpdateResult = invoke_http(classServiceURL, method = 'PUT')
    print("Class service update result code")
    print(classUpdateResult['code'])

    # * 2. Invoke user service to update user booking
    

    # * 3. Sending msg thru AMQP to message service
    print('\n\n-----Backend updated, publishing the (class booking) message with routing_key=email.info-----')
    # notification is listening to email_service queue
    # binding key is email.info as well

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
    #     "userEmail" : "celov54484@gpipes.com",
    #     "userName" : "celo",
    #     "orderID" : "4500",
    #     "courseName" : "Data Structure Algorithms",
    #     "coursePrice" : "$2000",
    #     "courseDescription" : "A 3rd semester course at SMU, continues to develop students' understanding of object oriented programming, memory management",
    #     "classId" : 3,
    #     "runId": 1,
    #     "userId": 10,
    #     }
    # )


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " to coordinate payments with updating of class and user services")
    app.run(host="0.0.0.0", port=5008, debug=True)
print(f"Flask app is initialized on port 5008")
