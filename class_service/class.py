import os

from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from os import environ
from pymongo import MongoClient
from bson import json_util
import sys


from datetime import datetime
import json

monitorBindingKey='booking.*'
app = Flask(__name__)
portNum = 5006
# Switches between DB_ENVIRONMENT and localhost depending on whether the app is running on docker or not
DB_ENVIRONMENT = environ.get('DB_ENVIRONMENT') or 'localhost'
client = MongoClient(host=DB_ENVIRONMENT,
                    port=27017
                    )

# client = MongoClient(host='localhost',
#                      port=27017
#                      )

CORS(app)

db = client['class_db']
sample_data = [
    {
        "_id": "1",
        "coursename": "CAD-Engineering-Design-5",
        "content": "On completion of the module, students should be able to create 2D drawings of engineering components using a CAD system as well as produce 3D solid models and also to design a mechanical system comprising various machine elements.\r\n\r\nCAD and Engineering Design (ME4011FP) is one of the modules leading to HIGHER NITEC IN TECHNOLOGY - MECHANICAL ENGINEERING.",
        "objective": "On completion of the module, students should be able to create 2D drawings of engineering components using a CAD system as well as produce 3D solid models and also to design a mechanical system comprising various machine elements.",
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
        "_id": "2",
        "coursename": "Advanced-Certificate-Data-Protection-Operational-Excellence-Module-2-Information-Cyber-Security-Managers-EXIN-Certification-Synchronous-Elearning",
        "content": "What You Will Be Learning\r\n-Understand the relationship between Information and security: the concept, the value, the importance and the reliability of information\r\n\r\n-Understand threats and risks: the concepts of threat and risk and the relationship with the reliability of information;\r\n\r\n-Learn the approach to secure your organization: the security policy and security organization including the components of the security organization and management of (security) incidents\r\n\r\n-Learn the measures to secure your organisation: the importance of security measures including physical, technical and organizational measures\r\n\r\n-Understand legislation and regulations: the importance and impact of legislation and regulations",
        "objective": "Understand the relationship between Information and security: the concept, the value, the importance and the reliability of information",
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
        "_id": "3",
        "coursename": "Advanced-Information-Management-Classroom-Asynchronous",
        "content": "Define a coherent data strategy and spearhead new approaches to enrich, synthesise and apply data, to maximise the value of data as a critical business asset and driver.",
        "objective": "Define a coherent data strategy and spearhead new approaches to enrich, synthesise and apply data, to maximise the value of data as a critical business asset and driver.",
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
        "_id": "4",
        "coursename": "Drive-Highly-Engaging-Online-Learning-Experience-Synchronous-eLearning",
        "content": "As trainers and educators invest in new technology and technical skills to move their training from in-person to online, it is important that learning remains engaging and meaningful for participants. How can trainers connect with their learners online and engage them in impactful learning? Learn key techniques to driving high engagement in online learning. Make full use of the learning platform and its' functions to design and deliver engaged learning that has learners connecting with themselves, each other, the topic and you.",
        "objective": "Learn key techniques to driving high engagement in online learning. Make full use of the learning platform and its' functions to design and deliver engaged learning that has learners connecting with themselves, each other, the topic and you.",
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
        "_id": "5",
        "coursename": "Robotics-Process-Automation-Begins-Synchronous-elearning-2",
        "content": "Robotics Process Automation (RPA) is the technology that enables computer software to emulate and integrate actions typically performed by us (humans) interacting with digital systems (e.g. a computer). The software that executes these actions is termed a “robot”. Examples of tasks that RPA robots are able to automate include capturing data, running applications and communicating with other systems. By automating processes that are highly manual, repetitive and rules-based, RPA solutions can yield greater productivity, create efficiency and reduce costs. Common internal processes across industries (such as banking, retail, tech and the government) that can benefit from RPA include HR, IT services, supply chain, finance and accounting, and customer management.\n\nThe programme aims to introduce robotics process automation to participants, and impart basic proficiency in RPA tools so that they are able to design their own RPA bots to automate common work processes in their organisations, upon completion of the course.",
        "objective": "Introduce robotics process automation to participants, and impart basic proficiency in RPA tools so that they are able to design their own RPA bots to automate common work processes in their organisations, upon completion of the course.",
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
    },
    {
        "_id": "6",
        "coursename": "Senior-Strength-and-Conditioning",
        "content": "This 2-days course will give you the practicals skills and knowledge to move forward with confidence in writing and delivering programs to senior clients at any level of physical competence",
        "objective": "Assessments as Exercises Patterns for Competency and Confidence",
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
        "fees":790,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["Health", "Fitness", "Senior", "Strength"]
    },
    {
        "_id": "7",
        "coursename": "Sports-Massage-Therapy",
        "content": "The general public is becoming more aware of the alternative therapies available for musculoskeletal injuries. Injuries do not only occur when participating in physical activity. Prolonged sitting and being deskbound can take a toll on one's well-being if left unchecked.",
        "objective": "Learn new skills and knowledge on how one can assist in facilitating the recovery from musculoskeletal injuries. Gain a better understanding to what the body may experience during injuries. Learn new skills and knowledge on how one can assist in facilitating the recovery.",
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
        "fees":700,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["Health", "Fitness", "Massage", "Sports"]
    },
    {
        "_id": "8",
        "coursename": "Maximising-Running-Performance",
        "content": "You will finish this 2-days course with an understanding of the science, programming and practical competencies required to program for, and train runners to personal best performances.",
        "objective": "Learn exercise prescription, programming weekly units of training, Master the art and technique of running and the strength training behind superior performance. The mobilisation techniques required to achieve or maintain symmetry in running and maintain healthy fascial and muscular integrity. Identify running faults and making the right decisions on how to fix them",
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
        "fees":900,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["Health", "Fitness", "Running", "Performance"]
    },
    {
        "_id": "9",
        "coursename": "Science-To-Gym-Floor",
        "content": "Build a foundational understanding of concepts in physiology, body composition, strength, performance, and nutrition. Recall various structural (anatomical) and functional (physiological) concepts that are relevant to exercise and nutrition application.",
        "objective": "Science to Gym Floor is a two-day learning experience for exercise professionals looking to gain a comprehensive understanding of the science behind training and nutrition, and its practical application.",
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
        "fees":900,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["Health", "Gym", "Exercise", "Performance"]
    },
    {
        "_id": "10",
        "coursename": "Workplace-Safety-and-Health-Practices",
        "content": "This course is assessment only (No training), and is designed specifically for cleaning stewards who are already working in the environmental services industry, and who understands the importance of the Workplace Safety and Health Act and practices at the workplace.",
        "objective": "This AOP will equip the participants with the necessary knowledge on how to understand and observe workplace safety through adherence to organisational guidelines and regulatory requirements",
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
        "fees":100,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["Workplace", "Safety", "Organisation", "Environment"]
    },
    {
        "_id": "11",
        "coursename": "L2-Washroom-Maintenance",
        "content": "Methods to remove stubborn stains in washroom facilities; Periodic maintenance or checks of washroom facilities; Appropriate PPE; Organisational procedures relating to the use of special and/or corrosive detergent to remove stubborn stains; Placement of signages; Types and proper use of cleaning tools, equipment and supplies; Types of special cleaning chemicals and their colour coding for cleaning washroom facilities; Wirkplace Safety and Health Act; Public Utilities (Water Supply) Regulation 38=9.",
        "objective": "Apply advanced cleaning and perform maintenance of washroom facilities.",
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
        "fees":1200,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["Workplace", "Washroom", "Organisation", "Maintainance"]
    },
    {
        "_id": "12",
        "coursename": "Environmental-Control-Coordinator-Course",
        "content": "This course will equip participants with the knowledge and skills to develop and implement an environmental sanitation programme for their workplace, which includes baseline standards such as cleaning frequencies, cleaning and disinfection protocols, pest management, etc. Participants who complete this program will be able to register with NEA and perform their duty as Environmental Control Coordinators.",
        "objective": "By the end of the course, the participants would be able to understand the importance of the Environmental Sanitation Regime, the roles of key stakeholders i.e. Premises Managers and Environmental Control Coordinators, and an overview of pest management, cleaning and disinfection, and indoor air quality, to draft and oversee the implementation of an Environmental Sanitation Programme as Environmental Control Coordinators. The participants will be equipped with the essential knowledge and skills to perform their duties and for obtaining an ECC certificate of registration.",
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
        "fees":450,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["Workplace", "Environment", "Organisation", "Sanitation"]
    },
    {
        "_id": "13",
        "coursename": "Operate-Waste-Collection-Vehicle-to-Collect-Waste",
        "content": "On completion of this unit, learners will have the knowledge and application skills in preparing for work activities for collecting waste, preparing vehicles (hook lift and rear end loader) for waste collection to collect waste and reinstating work area and vehicle at depot / heavy vehicle park.",
        "objective": "On completion of this unit, learners will have the knowledge and application skills in preparing for work activities for collecting waste, preparing vehicles (hook lift and rear end loader) for waste collection to collect waste and reinstating work area and vehicle at depot / heavy vehicle park.",
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
        "fees":450,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["Workplace", "Environment", "Waste", "Collection"]
    },
    {
        "_id": "14",
        "coursename": "Washroom-Maintenance",
        "content": "Understand requirements of Perform basic cleaning of washrooms (CLG-CPR-101E-1) with the knowledge and skills required in daily cleaning and removing soilage from sanitary fixtures, fittings, toilet floors, and replenishing consumables in sanitary area.",
        "objective": "In completion of this unit, the learner will have knowledge and application skills in the workplace. ",
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
        "fees":4050,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["Workplace", "Washroom", "Maintainance", "Cleanliness"]
    },
    {
        "_id": "15",
        "coursename": "Customer-Management",
        "content": "Develop the ability to collaborate with customers to achieve service outcomes.",
        "objective": "Collaborate with customers to provide service follow up. Analyse gaps between actual service performance and organisation’s service standards. Deploy service quality improvement tools to improve service delivery process.",
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
        "fees":40,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":True,
        # course category
        "category":["Workplace", "Business", "Customer", "Management"]
    }
]

# Initialize Mongo with sample data
@app.route('/createDB')
def create_db():
    db_exists = client.list_database_names()
    if 'class_db' in db_exists:
        client.drop_database('class_db')
    db = client['class_db']
    for data in sample_data:
        db["classes"].insert_one(data)
    return "Sample data inserted successfully" + str(sample_data)

# Health Check 
@app.route('/health', methods=('GET', 'POST'))
def index():
    return "Class Service is up and running"

# Get All classes
@app.route('/')
def get_all_classes():
    classes = db.classes.find()
    return json.loads(json_util.dumps(classes))

# Get class details from class Id
@app.route('/<classId>')
def get_class(classId):
    myquery = {"_id": classId}
    currClass = db.classes.find_one(myquery)
    if not currClass:
        return f"Class of _id: {classId} does not exist", 404
    return json.loads(json_util.dumps(currClass))

# get all unique class objects details for a specific user
@app.route('/getUserClass/<userId>')
def get_user_class(userId):
    matching_classes = {}
    returned_classes = []
    for class_doc in db.classes.find():
        for course_run in class_doc['courseRuns']:
            if userId in class_doc['courseRuns'][course_run]['participants'] and class_doc["coursename"] not in matching_classes:
                returned_classes.append(class_doc)
    return returned_classes

# Add user to class participants
@app.route('/<classId>/<runId>', methods=['PUT'])
def add_user_class(classId, runId):
    data = request.get_json()
    courseRun = f"courseRuns.{runId}.participants"
    courseRunSlots = f"courseRuns.{runId}.availableSlots"
    myquery = {"_id": classId}
    class_doc = db.classes.find_one(myquery)
    if not class_doc:
        return f"Class of _id: {classId} does not exist", 404
    print("class_doc is",  class_doc,file=sys.stderr)
    print("participants list is",class_doc["courseRuns"][runId]["participants"],file=sys.stderr)
    newvalues = {"$push": {courseRun: data['userId']},  "$inc": {
            courseRunSlots: -1}}
    if not newvalues:
        return f"Invalid class run of {runId}", 400
    if data['userId'] not in class_doc["courseRuns"][runId]["participants"]:
        updated_class = db.classes.find_one_and_update(myquery, newvalues)
        if not updated_class:
            return f"Invalid class run of {runId}", 400
    else:
        updated_class = class_doc
    return json.loads(json_util.dumps(updated_class))


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +": manage class Schedule ...")
    create_db()
    app.run(host='0.0.0.0', port=portNum, debug=True)
print(f"Class Service app is initialized on port {portNum}")