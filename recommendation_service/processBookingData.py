import json
from confluent_kafka import Consumer, KafkaError
from contentBasedFilter import ContentBasedFilter
from kafka import KafkaProducer
from json import dumps
import sys


producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

c = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'latest'
})

c.subscribe(['booking'])

def main():
    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {}'.format(msg.topic()))
                continue
            else:
                print('Error while consuming message: {}'.format(msg.error()))
                continue
        else:
            print('Received message: {}'.format(msg.value().decode('utf-8')))
            history = msg.value().decode('utf-8')
            print("History is",json.loads(history))
            latestBooking = json.loads(history)
            recommendations = ContentBasedFilter.get_recommendations(latestBooking["className"].strip())
            recommendObj = {
                "userId" : latestBooking["userId"],
                "recommendation" : recommendations
            }
            print("------- recommendation received is --------",file=sys.stderr)
            print(recommendObj,file=sys.stderr)
            producer.send('recommendations', recommendObj)

if __name__ == '__main__':
    main()