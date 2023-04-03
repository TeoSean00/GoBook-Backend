import os

from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from os import environ
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

from datetime import datetime
import json

monitorBindingKey='booking.*'
app = Flask(__name__)

# for docker | for local
client = environ.get('class_db') or MongoClient(host='localhost',
                    port=27017
                    )

# client = MongoClient(host='localhost',
#                      port=27017
#                      )
portNum = 5006
db = client['class_db']
sample_data = [
    {
        "className": "CAD-Engineering-Design-5",
        "content": "On completion of the module, students should be able to create 2D drawings of engineering components using a CAD system as well as produce 3D solid models and also to design a mechanical system comprising various machine elements.\r\n\r\nCAD and Engineering Design (ME4011FP) is one of the modules leading to HIGHER NITEC IN TECHNOLOGY - MECHANICAL ENGINEERING.",
        "objective": "On completion of the module, students should be able to create 2D drawings of engineering components using a CAD system as well as produce 3D solid models and also to design a mechanical system comprising various machine elements.",
         "participants": [
        ],
        "categories": ["SSG-Non-WSQ"],
        "classSize": 25,
        # displayed as pills for each date
        "courseRuns":{
            "1": {
                "date": "2023-4-12",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ]},
            "2":{
                "date": "2023-4-12",
                "timeslot" : "12.00pm - 3.00pm",
                "availableSlots": 25,
                "participants": [
                ], },
            "3":{
                "date": "2023-4-13",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ], },
            "4":{
                "date": "2023-4-13",
                "timeslot" : "12.00pm - 3.00pm",
                "availableSlots": 25,
                "participants": [
                ], },
            "5":{
                "date": "2023-4-14",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ], }
        },
        "fees": 1620,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment": True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification": True,
        # course category
        "category": ["Engineering", "CAD", "System"]
    },
    {
        "className": "Advanced-Certificate-Data-Protection-Operational-Excellence-Module-2-Information-Cyber-Security-Managers-EXIN-Certification-Synchronous-Elearning",
        "content": "What You Will Be Learning\r\n-Understand the relationship between Information and security: the concept, the value, the importance and the reliability of information\r\n\r\n-Understand threats and risks: the concepts of threat and risk and the relationship with the reliability of information;\r\n\r\n-Learn the approach to secure your organization: the security policy and security organization including the components of the security organization and management of (security) incidents\r\n\r\n-Learn the measures to secure your organisation: the importance of security measures including physical, technical and organizational measures\r\n\r\n-Understand legislation and regulations: the importance and impact of legislation and regulations",
        "objective": "Understand the relationship between Information and security: the concept, the value, the importance and the reliability of information",
        "participants": [
        ],
        "classSize":30,
        "courseRuns":{
            "1": {
                "date": "2023-4-12",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ]},
            "2":{
                "date": "2023-4-12",
                "timeslot" : "12.00pm - 3.00pm",
                "availableSlots": 25,
                "participants": [
                ], },
            "3":{
                "date": "2023-4-13",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ], },
            "4":{
                "date": "2023-4-13",
                "timeslot" : "12.00pm - 3.00pm",
                "availableSlots": 25,
                "participants": [
                ], },
            "5":{
                "date": "2023-4-14",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ], }
        },
        "fees":1620,
        "assessment":True,
        "certification":False,
        "category":["Data", "PDPA", "Cyber"]
    },
    {   
        "className": "Advanced-Information-Management-Classroom-Asynchronous",
        "content": "Define a coherent data strategy and spearhead new approaches to enrich, synthesise and apply data, to maximise the value of data as a critical business asset and driver.",
        "objective": "Define a coherent data strategy and spearhead new approaches to enrich, synthesise and apply data, to maximise the value of data as a critical business asset and driver.",
        "participants": [
        ],
        "classSize":30,
        "courseRuns":{
            "1": {
                "date": "2023-4-12",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ]},
            "2":{
                "date": "2023-4-12",
                "timeslot" : "12.00pm - 3.00pm",
                "availableSlots": 25,
                "participants": [
                ], },
            "3":{
                "date": "2023-4-13",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ], },
            "4":{
                "date": "2023-4-13",
                "timeslot" : "12.00pm - 3.00pm",
                "availableSlots": 25,
                "participants": [
                ], },
            "5":{
                "date": "2023-4-14",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ], }
        },
        "fees":1420,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":False,
        # course category
        "category":["Technology", "Data", "Process", "Security"]
    },
    {
        "className": "Drive-Highly-Engaging-Online-Learning-Experience-Synchronous-eLearning",
        "content": "As trainers and educators invest in new technology and technical skills to move their training from in-person to online, it is important that learning remains engaging and meaningful for participants. How can trainers connect with their learners online and engage them in impactful learning? Learn key techniques to driving high engagement in online learning. Make full use of the learning platform and its' functions to design and deliver engaged learning that has learners connecting with themselves, each other, the topic and you.",
        "objective": "Learn key techniques to driving high engagement in online learning. Make full use of the learning platform and its' functions to design and deliver engaged learning that has learners connecting with themselves, each other, the topic and you.",
        "participants": [
        ],
        "classSize":20,
        "courseRuns":{
            "1": {
                "date": "2023-4-12",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ]},
            "2":{
                "date": "2023-4-12",
                "timeslot" : "12.00pm - 3.00pm",
                "availableSlots": 25,
                "participants": [
                ], },
            "3":{
                "date": "2023-4-13",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ], },
            "4":{
                "date": "2023-4-13",
                "timeslot" : "12.00pm - 3.00pm",
                "availableSlots": 25,
                "participants": [
                ], },
            "5":{
                "date": "2023-4-14",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ], }
        },
        "fees":1420,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":False,
        # course category
        "category":["Technology", "Education", "Engage"]
    },
    {
        "className": "Robotics-Process-Automation-Begins-Synchronous-elearning-2",
        "content": "Robotics Process Automation (RPA) is the technology that enables computer software to emulate and integrate actions typically performed by us (humans) interacting with digital systems (e.g. a computer). The software that executes these actions is termed a “robot”. Examples of tasks that RPA robots are able to automate include capturing data, running applications and communicating with other systems. By automating processes that are highly manual, repetitive and rules-based, RPA solutions can yield greater productivity, create efficiency and reduce costs. Common internal processes across industries (such as banking, retail, tech and the government) that can benefit from RPA include HR, IT services, supply chain, finance and accounting, and customer management.\n\nThe programme aims to introduce robotics process automation to participants, and impart basic proficiency in RPA tools so that they are able to design their own RPA bots to automate common work processes in their organisations, upon completion of the course.",
        "objective": "Introduce robotics process automation to participants, and impart basic proficiency in RPA tools so that they are able to design their own RPA bots to automate common work processes in their organisations, upon completion of the course.",
        "participants": [
        ],
        "classSize":30,
        "courseRuns":{
            "1": {
                "date": "2023-4-12",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ]},
            "2":{
                "date": "2023-4-12",
                "timeslot" : "12.00pm - 3.00pm",
                "availableSlots": 25,
                "participants": [
                ], },
            "3":{
                "date": "2023-4-13",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ], },
            "4":{
                "date": "2023-4-13",
                "timeslot" : "12.00pm - 3.00pm",
                "availableSlots": 25,
                "participants": [
                ], },
            "5":{
                "date": "2023-4-14",
                "timeslot" : "10.00am - 11.00am",
                "availableSlots": 25,
                "participants": [
                ], }
        },
        "fees":1990,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["RPA", "Automation", "Process", "Robotics"]
    }
]


CORS(app)

# This API is to initialize the document in Mongo and fill with sample data
@app.route('/class/createDB')
def create_db():
    db_exists = client.list_database_names()
    if 'class_db' in db_exists:
        client.drop_database('class_db')
    db = client['class_db']
    for data in sample_data:
        db["classes"].insert_one(data)
    return "Sample data inserted successfully" + str(sample_data)

# Testing Route 
@app.route('/', methods=('GET', 'POST'))
def index():
    return "Hello there, there are the classes"

# This API will get all classes
@app.route('/class')
def get_all_classes():
    classes = db.classes.find()
    return json.loads(json_util.dumps(classes))


# get class details from class Id
@app.route('/class/<classId>')
def get_class(classId):
    object = ObjectId(classId)
    myquery = {"_id": object}
    currClass = db.classes.find_one(myquery)
    return json.loads(json_util.dumps(currClass))

# add user to class participants
@app.route('/class/<classId>/<runId>', methods=['PUT'])
def add_user_class(classId, runId):
    # This will be a the json put in the request. Use postman to add the partcipant using PUT
    print("start class update")
    data = request.get_json()
    data = json.loads(data)
    object = ObjectId(classId)
    courseRun = f"courseRuns.{runId}.participants"
    courseRunSlots = f"courseRuns.{runId}.availableSlots"
    myquery = {"_id": object}
    # update overall class list and course run class list
    newvalues = {"$push": {"participants": data['userId'],courseRun: data['userId']},  "$inc": {
        courseRunSlots: -1}}
    updated_class = db.classes.find_one_and_update(myquery, newvalues)
    return json.loads(json_util.dumps(updated_class))


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": manage class Schedule ...")
    app.run(host='0.0.0.0', port=portNum, debug=True)
print(f"Class Service app is initialized on port {portNum}")