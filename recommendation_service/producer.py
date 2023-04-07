import json
from kafka import KafkaProducer
from json import dumps
import time
import logging

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

####################
p = KafkaProducer(bootstrap_servers=['localhost:29092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))
print("Kafka Producer has been initiated...")

####################

f = [
    {
        "coursename": "CAD-Engineering-Design-5",
        "userId": "user1"
    },
    {
        "coursename": "Advanced-Certificate-Data-Protection-Operational-Excellence-Module-2-Information-Cyber-Security-Managers-EXIN-Certification-Synchronous-Elearning",
        "userId": "user2"
    },
    {
        "coursename": "Advanced-Information-Management-Classroom-Asynchronous",
        "userId": "user3"
    },
    {
        "coursename": "Drive-Highly-Engaging-Online-Learning-Experience-Synchronous-eLearning",
        "userId": "user2"
    },
    {
        "coursename": "Robotics-Process-Automation-Begins-Synchronous-elearning-2",
        "userId": "user3"
    }
]

def main():
    for classData in f:
        # classData = classObj["coursename"]
        p.send('booking', classData)
        p.flush()
        time.sleep(3)  # Add a delay to simulate streaming

if __name__ == '__main__':
    main()