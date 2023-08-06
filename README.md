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
