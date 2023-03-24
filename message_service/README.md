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
docker run -p 3000:3000 messaging_service
```
