import random
import time
import pika
import csv
import json

class DataEmitter:
    def __init__(self, csv_file_path, max_attempts=3, retry_delay=5):
        self.csv_file_path = csv_file_path
        self.max_attempts = max_attempts
        self.retry_delay = retry_delay

        self.connection = None
        self.channel = None

    def connect_to_rabbitmq(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            self.channel = self.connection.channel()
            
            # declare exchange
            self.channel.exchange_declare(exchange='wikipedia_edits', exchange_type='direct')

            # declare queue
            self.channel.queue_declare(queue='wikipedia_queue')

            #binding the queue to the exchange and routing key
            self.channel.queue_bind(exchange='wikipedia_edits', queue='wikipedia_queue', routing_key='wikipedia_key')
            print("Connected to RabbitMQ server.")
            return True

        except pika.exceptions.AMQPConnectionError:
            print("Error connecting to RabbitMQ server.")
            return False

    def disconnect_from_rabbitmq(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def process_csv_file(self):
        with open(self.csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header line that has the column names

            for row in csv_reader:
                data = dict(zip(["", "$schema", "id", "type", "namespace", "title", "comment", "timestamp", "user",
                                 "bot", "minor", "patrolled", "server_url", "server_name", "server_script_path",
                                 "wiki", "parsedcomment", "meta_domain", "meta_uri", "meta_request_id",
                                 "meta_stream", "meta_topic", "meta_dt", "meta_partition", "meta_offset", "meta_id",
                                 "length_old", "length_new", "revision_old", "revision_new"], row))

                time.sleep(random.random())
                message_data = {
                    "timestamp": data['meta_dt'],
                    "server_name": data["server_name"]
                }
                message_body = json.dumps(message_data)

                source = data["server_name"]
                if "de.wikipedia.org" in source:
                    self.send_message(message_body, "German Wikipedia")
                else:
                    self.send_message(message_body, "Global Wikipedia")

    def send_message(self, message_body, source):
        try:
            self.channel.basic_publish(exchange='wikipedia_edits', routing_key='wikipedia_key', body=message_body)
            print(f"Sending message for {source}")
        except Exception as e:
            print(f"Error occurred while sending message for source '{source}': {str(e)}")

    def run(self):
        attempts = 0
        while attempts < self.max_attempts:
            if self.connect_to_rabbitmq():
                try:
                    self.process_csv_file()
                except KeyboardInterrupt:
                    print("Producer interrupted.")
                    break
                except Exception as e:
                    print(f"Error occurred: {str(e)}")
                finally:
                    self.disconnect_from_rabbitmq()
                    break
            else:
                attempts += 1
                if attempts < self.max_attempts:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    print("Max attempts reached. Exiting...")
                    break

if __name__ == "__main__":
    data_emitter = DataEmitter('de_challenge_sample_data.csv')
    data_emitter.run()
