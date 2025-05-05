import pika
from config import RABBITMQ_HOST, RABBITMQ_QUEUE, RABBITMQ_USER, RABBITMQ_PASS
import logging
import time


logging.basicConfig(level=logging.INFO)


# function is triggered whenever a new message arrives in the queue. It decodes the message and simulates sending a notification.
def callback(ch, method, properties, body):
    #simulate: Logging that a booking message was received.
    print(f"[Notification Service] Received message: {body.decode()}") #converts the byte message to a string.
    #simulate: Simulating an email notification to the user.
    print("[Notification Service] Sending email to user (simulated)...")
    logging.info(f"Received message from queue: {body.decode()}")

def start_consumer(max_retries=10, delay_seconds=5):
    connection = None
    for attempt in range(max_retries):
        try:
            logging.info(f"Attempting to connect to RabbitMQ at {RABBITMQ_HOST} (attempt {attempt + 1})")
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
            #Connects to the RabbitMQ server.
            connection = pika.BlockingConnection(parameters)
            break
        except pika.exceptions.AMQPConnectionError as e:
            logging.warning(f"Connection failed: {e}. Retrying in {delay_seconds} seconds...")
            time.sleep(delay_seconds)
    else:
        logging.error("Failed to connect to RabbitMQ after multiple attempts.")
        return
    
    #Creates a channel (a lightweight connection on top of TCP)
    channel = connection.channel()
    #Declares the queue (in case it doesn’t exist already)
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    #Subscribes to that queue using basic_consume, registering the callback.
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
    print(f"[Notification Service] Waiting for messages in '{RABBITMQ_QUEUE}'...")
    #enter an infinite loop and keep listening for messages.
    channel.start_consuming()