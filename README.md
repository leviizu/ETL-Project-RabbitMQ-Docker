# RabbitMQ-ETL-and-Analysis
A client, a media house, is interested in current trends on Wikipedia and historical changes of topics. 
For this purpose, all changes made to Wikipedia are to be stored, processed and the results presented in a dashboard.
A system is planned, which provides the change events with the help of RabbitMQ and writes them to a CSV,
where they can be analysed with a suitable query engine.

## Task
A RabbtiqMQ instance is to be set up as a prototype to test and demonstrate possible scenarios.
Within the scope of the prototype, the following components are to be programmed as part of the prototype:

● A producer that reads in the sample data(de_challenge_sample_data.csv) and emits it at random intervals between 0-1 second. 

● A RabbitMQ Consumer that reads this data from a queue, performs the following aggregations and stores the results:

#### Global number of edits per minute.
#### Number of edits of the German Wikipedia per minute


Setting up RabbitMQ with Docker Compose
This repository contains a RabbitMQ prototype setup with Docker Compose, consisting of a producer and a consumer for testing and demonstrating possible scenario.

The goal of this project is to create a system that collects and processes Wikipedia edit events, calculates the global number of edits per minute, and also tracks the number of edits for the German Wikipedia per minute. The system uses RabbitMQ as the message broker to handle the message passing between the producer and consumer.

Setup
Clone the repository to your local machine.

Install Docker Desktop and make sure it's running.

Open the project folder in Visual Studio Code (optional but recommended).

Project Structure
The repository has the following files:

docker-compose.yml: The Docker Compose configuration file that defines the RabbitMQ server, producer, and consumer services.

Dockerfile_producer and Dockerfile_consumer: Dockerfiles for building the Docker images for the producer and consumer scripts.

producer.py: The Python script acting as the producer, emitting sample data to the RabbitMQ queue.

consumer.py: The Python script acting as the consumer, reading data from the RabbitMQ queue and performing aggregations.

How to Run
Open the terminal in Visual Studio Code or any terminal/command prompt in the project folder.

Run the following command to build the Docker images and start the containers:

docker-compose up --build

This command will start the RabbitMQ server and the producer and consumer containers, and you'll see the logs in the terminal.

Note
To stop the containers, press 'Ctrl+C' in the terminal where the Docker Compose is running.

To remove the Docker containers and images created by Docker Compose, run the following command:

docker-compose down
