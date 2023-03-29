# Messaging Service
The Messaging Service sends out a email to the user upon booking confirmation. The email contains the booking details and a eticket in the form of a PDF.

## Installation
1. Install the dependencies
```
npm install
```
2. Start up the MongoDB server and AMQP on your local machine


3. Run the server
```
npm start
```


## Usage
1. To TEST send a POST request to the server with the following body to the endpoint `/test`:
```
{
    "userEmail" : "yourEmail@gmail.com",
    "userName" : "yourName",
    "orderID" : "1001",
    "courseName" : "Data Structure Algorithms",
    "coursePrice" : "$2000",
    "courseDescription" : "A 3rd semester course at SMU, continues to develop students' understanding of object oriented programming, memory management"
}
```
2. This microservice is meant to take a json object from the AMQP and will trigger a callback function to send the email to the user. To TEST this, run the update booking microservice

###
1. Docker Build
```
docker build . -t messaging_service
```
2. Docker Run (Change the ports as you wish)
```
docker run -p 5010:5010 messaging_service
```

#### ENV for testing
```
module.exports = {
  EMAIL: "esdg07t01@gmail.com",
  PASSWORD: "ackxcbcupcpcrhvh",
  dbUri: "mongodb://localhost:27017/messaging",
  port: 5010,
  rabbitMQ: "amqp://localhost:5672",
  queueName: "email_service",
};
```

#### ENV for production
```
module.exports = {
  EMAIL: "esdg07t01@gmail.com",
  PASSWORD: "ackxcbcupcpcrhvh",
  dbUri: "mongodb://message_db:27019/messaging",
  port: 5010,
  rabbitMQ: "amqp://rabbitmq:5672",
  queueName: "email_service",
};
```