from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))


f = [
    {
        "className": "CAD-Engineering-Design-5",
        "content": "On completion of the module, students should be able to create 2D drawings of engineering components using a CAD system as well as produce 3D solid models and also to design a mechanical system comprising various machine elements.\r\n\r\nCAD and Engineering Design (ME4011FP) is one of the modules leading to HIGHER NITEC IN TECHNOLOGY - MECHANICAL ENGINEERING.",
        "objective": "On completion of the module, students should be able to create 2D drawings of engineering components using a CAD system as well as produce 3D solid models and also to design a mechanical system comprising various machine elements.",
        "categories": ["SSG-Non-WSQ"],
        "classSize": 25,
        # displayed as pills for each date
        "courseRuns":{
            1: {
                "date": "21/06 - 24/06",
                "availableSlots": 25,
                "participants": [
                ]},
            2:{
                "date": "07/07 - 10/07",
                "availableSlots": 25,
                "participants": [
                ], },
            3:{
                "date": "11/08 - 14/08",
                "availableSlots": 25,
                "participants": [
                ], },
            4:{
                "date": "16/08 - 19/08",
                "availableSlots": 25,
                "participants": [
                ], },
            5:{
                "date": "21/10 - 24/10",
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
        "availableSlots":12,
        "courseRuns":{
            1: {
                "date": "21/06 - 24/06",
                "availableSlots": 25,
                "participants": [
                ]},
            2:{
                "date": "07/07 - 10/07",
                "availableSlots": 25,
                "participants": [
                ], },
            3:{
                "date": "11/08 - 14/08",
                "availableSlots": 25,
                "participants": [
                ], },
            4:{
                "date": "16/08 - 19/08",
                "availableSlots": 25,
                "participants": [
                ], },
            5:{
                "date": "21/10 - 24/10",
                "availableSlots": 25,
                "participants": [
                ], }
        },
        "fees":1620,
        # if assessment true, display "An assessment will be conducted at the end of the course."
        "assessment":True,
        # if true display "Upon completion of all 6 modules within a maximum duration of 3 years, participants will be awarded a digital Certificate in Professional Certificate in Python Programming."
        "certification":False,
        # course category
        "category":["Data", "PDPA", "Cyber"]
    },
    {
        "className": "Advanced-Information-Management-Classroom-Asynchronous",
        "content": "Define a coherent data strategy and spearhead new approaches to enrich, synthesise and apply data, to maximise the value of data as a critical business asset and driver.",
        "objective": "Define a coherent data strategy and spearhead new approaches to enrich, synthesise and apply data, to maximise the value of data as a critical business asset and driver.",
        "participants": [
        ],
        "classSize":30,
        "availableSlots":20,
        "courseRuns":{
            1: {
                "date": "21/06 - 24/06",
                "availableSlots": 25,
                "participants": [
                ]},
            2:{
                "date": "07/07 - 10/07",
                "availableSlots": 25,
                "participants": [
                ], },
            3:{
                "date": "11/08 - 14/08",
                "availableSlots": 25,
                "participants": [
                ], },
            4:{
                "date": "16/08 - 19/08",
                "availableSlots": 25,
                "participants": [
                ], },
            5:{
                "date": "21/10 - 24/10",
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
        "availableSlots":10,
        "courseRuns":{
            1: {
                "date": "21/06 - 24/06",
                "availableSlots": 25,
                "participants": [
                ]},
            2:{
                "date": "07/07 - 10/07",
                "availableSlots": 25,
                "participants": [
                ], },
            3:{
                "date": "11/08 - 14/08",
                "availableSlots": 25,
                "participants": [
                ], },
            4:{
                "date": "16/08 - 19/08",
                "availableSlots": 25,
                "participants": [
                ], },
            5:{
                "date": "21/10 - 24/10",
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
        "availableSlots":20,
        "courseRuns":{
            1: {
                "date": "21/06 - 24/06",
                "availableSlots": 25,
                "participants": [
                ]},
            2:{
                "date": "07/07 - 10/07",
                "availableSlots": 25,
                "participants": [
                ], },
            3:{
                "date": "11/08 - 14/08",
                "availableSlots": 25,
                "participants": [
                ], },
            4:{
                "date": "16/08 - 19/08",
                "availableSlots": 25,
                "participants": [
                ], },
            5:{
                "date": "21/10 - 24/10",
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

for classObj in f:
    classData = classObj["className"]
    producer.send('booking', classData)
    time.sleep(5)  # Add a delay to simulate streaming
