import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq") #fallback values (localhost, etc.) are helpful for testing outside Docker.
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "booking_queue")