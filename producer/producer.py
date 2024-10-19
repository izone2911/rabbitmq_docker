import json
import pika
import os

# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

# connect to rabbitmq
connection = pika.BlockingConnection(url_params)
chan = connection.channel()

# declare a new queue
# durable flag is set so that messages are retained
# in the rabbitmq volume even between restarts
chan.queue_declare(queue='hello', durable=True)

dict = {"id":11, "packet_no":126, "temperature":30, "humidity":60, "tds":1100, "pH":5.0}
# publish a 100 messages to the queue
for i in range(1):
    chan.basic_publish(exchange='', routing_key='hello',
                       body= json.dumps(dict), properties=pika.BasicProperties(delivery_mode=2))
    print("Produced the message")

# close the channel and connection
# to avoid program from entering with any lingering
# message in the queue cache
chan.close()
connection.close()
