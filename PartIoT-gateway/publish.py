
from flask import jsonify
import json

# publish.py
import pika, os

def init_connection():
    # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='temperature') # Declare a queue
    return connection, channel

def publish_temperature(channel, temperature: int, id: int):
    bodyjson = json.dumps({ 'temperature': temperature, 'id': id })
    channel.basic_publish(exchange='',
                      routing_key='temperature',
                      body=bodyjson)


def cleanup(connection):
    connection.close()