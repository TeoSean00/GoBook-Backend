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

CORS(app)  

client = MongoClient(host='localhost',
                        port=27017
                        )

# 