from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer('recommendations',
                         bootstrap_servers=['localhost:29092'],
                         auto_offset_reset='earliest',
                         group_id='mygroup',
                         enable_auto_commit=True,
                         value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    print(message.value)