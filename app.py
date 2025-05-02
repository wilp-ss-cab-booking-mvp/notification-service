#Just imports and starts the RabbitMQ consumer logic.
from consumer import start_consumer

#The entry point of the service.
if __name__ == "__main__":
    start_consumer()