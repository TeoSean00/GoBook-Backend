from confluent_kafka import Consumer, KafkaError
from contentBasedFilter import ContentBasedFilter
from tools import publish_message

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'latest'
})

c.subscribe(['booking'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached {}'.format(msg.topic()))
        else:
            print('Error while consuming message: {}'.format(msg.error()))
    else:
        print('Received message: {}'.format(msg.value().decode('utf-8')))
        history = msg.value().decode('utf-8')
        recommendations = ContentBasedFilter.get_recommendations(history)
        publish_message('recommendations', ', '.join(recommendations))