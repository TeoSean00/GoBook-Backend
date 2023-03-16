import os

from flask import Flask, render_template, request, url_for, redirect,jsonify
import requests
from flask_cors import CORS
from os import environ
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

from datetime import datetime
import json

app = Flask(__name__)

CORS(app)  

client = MongoClient(host='localhost',
                        port=27017
                        )

#interact with payment service


@app.route('/booking/createPayment', methods=['POST'])
async def create_payment():
    data = request.get_json()
    class_output = []
    # This is for docker
    # user_data = requests.request("GET", "http://user_service:5001/users/" + userid)
    url = 'http://localhost:8080/create-payment-intent'
    response_data = requests.post(url,data)
    print("RESPONSE IS",response_data)
    return response_data

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": class booking service ...")
    app.run(host='0.0.0.0', port=5007, debug=True)