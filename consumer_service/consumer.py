from kafka import KafkaConsumer
from json import loads
from flask import Flask
from flask_socketio import SocketIO, emit
import os
import threading

app = Flask(__name__)
PORT = 5011
socketio = SocketIO(app,cors_allowed_origins="*")

consumer = KafkaConsumer('recommendations',
                         bootstrap_servers=['kafka:9092'],
                         auto_offset_reset='earliest',
                         group_id='mygroup',
                         enable_auto_commit=True,
                         value_deserializer=lambda x: loads(x.decode('utf-8')))

def kafka_listener():
    for message in consumer:
        print(message.value)
        socketio.emit('message', message.value)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": receiving Kafka recommendations ...")
    kafka_thread = threading.Thread(target=kafka_listener)
    kafka_thread.start()
    socketio.run(app, host='0.0.0.0', port=PORT, **{'allow_unsafe_werkzeug': True})