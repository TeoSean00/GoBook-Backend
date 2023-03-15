from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

p = Producer({'bootstrap.servers': 'localhost:9092'})

def publish_message(topic_name, value):
    try:
        p.produce(topic_name, value.encode('utf-8'), callback=delivery_report)
        p.flush()
    except Exception as e:
        print('Exception in publishing message')
        print(str(e))