import pika
import json
import time
from datetime import datetime
import csv

class DataConsumer:
    def __init__(self):
        self.global_edits_per_minute = []
        self.german_edits_per_minute = []

    def callback(self, ch, method, properties, body):
        try:
            # Convert the incoming message (body) to a JSON object
            message = json.loads(body)

            # Extract the timestamp and server name from the JSON object
            timestamp_str = message.get('timestamp')
            server_name = message.get('server_name')

            if not timestamp_str or not server_name:
                print("Missing required fields in the message.")
                return

            # Convert the timestamp string to a timestamp object
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            # Check if the edit is for the German Wikipedia
            if "de.wikipedia.org" in server_name:
                # Increment the German Wikipedia edits counter for this minute
                self.german_edits_per_minute.append((timestamp, 1))
            else:
                # Increment the global edits counter for this minute
                self.global_edits_per_minute.append((timestamp, 1))
        except Exception as e:
            print(f"Error occurred while processing message: {str(e)}")

    def consume_data(self):
        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
                channel = connection.channel()

                # Declaring the exchange and queue
                channel.exchange_declare(exchange='wikipedia_edits', exchange_type='direct')
                channel.queue_declare(queue='wikipedia_queue')

                # Bind the queue to the exchange with the appropriate routing key
                channel.queue_bind(exchange='wikipedia_edits', queue='wikipedia_queue', routing_key='wikipedia_key')

                # Set up the callback function to be triggered when a message is received
                channel.basic_consume(queue='wikipedia_queue', on_message_callback=self.callback, auto_ack=True)

                print('Waiting for messages. To exit, press CTRL+C')

                # Start consuming messages from the queue
                channel.start_consuming()

                connection.close()
                print("Connection closed")
                success = True

            except pika.exceptions.AMQPConnectionError:
                print(f"Error connecting to RabbitMQ server.")
                attempts += 1
                if attempts < 3:
                    print(f"Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Max attempts reached. Exiting...")
                    success = True

            except KeyboardInterrupt:
                print(f"Consumer interrupted.")
                success = True

            except Exception as e:
                print(f"Error occurred: {str(e)}")
                attempts += 1
                if attempts < 3:
                    print(f"Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Max attempts reached. Exiting...")
                    success = True


    def write_to_csv(self, filename, data):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Edits Count'])
            for timestamp, edits_count in data:
                writer.writerow([timestamp, edits_count])

        # After consuming all messages, write the aggregated edits per minute data to CSV files
        self.write_to_csv("global_edits_per_minute.csv", self.global_edits_per_minute)
        self.write_to_csv("german_edits_per_minute.csv", self.german_edits_per_minute)


if __name__ == "__main__":
    data_consumer = DataConsumer()
    data_consumer.consume_data()
