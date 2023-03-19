from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)
# ----------------- handle function call to this page --------
@app.route("/update_booking",methods=['POST'])
def update_booking():
    data = request.get_json()
    print('request data from process_booking: ',data)

    # flag and code for testing
    payment_successful,code = True, 200
    # payment_successful,code = False, 400


    # if payment response successful
    if payment_successful:
        print('\n\n-----Publishing the (class booking) message with routing_key=booking.info-----')
        # publish class details JSON message to rabbitMQ
        # which will update the backend

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="booking.info", 
            body=data, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # continue even if this invocation fails        
        print("\Booking info ({:d}) published to the RabbitMQ Exchange:".format(
            code), data)
        
        # then when response received from this update, fire off email
        # publish email message and JSON data to rabbitMQ
        
        print('\n\n-----Backend updated, publishing the (class booking) message with routing_key=email.info-----')
        # notification is listening to email_service queue 
        # binding key is email.info as well

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email.info", 
            body=data, properties=pika.BasicProperties(delivery_mode = 2)) 
        # No need to return response to process_booking
        return 

    
    # else if unsuccessful, fire email only
    else:
        # publish email message and JSON data to rabbitMQ
        print('\n\n-----Payment failed, publishing the (class booking) message with routing_key=email.info-----')
        # notification is listening to email_service queue 
        # binding key is email.info as well

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email.info", 
            body=data, properties=pika.BasicProperties(delivery_mode = 2)) 

    # No need to return response to process_booking

    return 



# -------------------------- EMAIL -------------------------------
# if this complex microservice, using AMQP can call message_service
# @app.route("/emailservice", methods=['POST'])
# def processEmailService():

#     order = request.get_json()
#     order_msg = json.dumps(order)
#     print("order msg is after this")
#     print(order_msg)
#     # Send the order object to the messaging microservice via RabbitMQ
#     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="message.", 
#             body=order_msg, properties=pika.BasicProperties(delivery_mode = 2))
    
#     # Test Return statement
#     return {
#         "code": 201,
#         "data": {
#             "order": "success"
#         }
#     }


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " to register for a class")
    app.run(host="0.0.0.0", port=5007, debug=True)
print(f"Flask app is initialized on port 5007")