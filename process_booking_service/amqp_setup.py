import pika
import os 
from os import environ

# These module-level variables are initialized whenever a new instance of python interpreter imports the module;
# In each instance of python interpreter (i.e., a program run), the same module is only imported once (guaranteed by the interpreter).
# ! For Docker 
hostname = "rabbitmq" # default hostname
port = 5672 # default port
# ? connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600,
))

channel = connection.channel()

exchangename="booking_topic"
exchangetype="topic"
channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)

############   email_Service queue    #############
#declare email_Service queue
queue_name = 'email_service'
channel.queue_declare(queue=queue_name, durable=True)


#bind email_Service queue
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='email.info') 


"""
This function in this module sets up a connection and a channel to a local AMQP broker,
and declares a 'topic' exchange to be used by the microservices in the solution.
"""
def check_setup():
    global connection, channel, hostname, port, exchangename, exchangetype

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, heartbeat=3600, blocked_connection_timeout=3600))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)


def is_connection_open(connection):
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False
