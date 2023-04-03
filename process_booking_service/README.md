# create_booking_complex_service

### To Run RabbitMQ Docker
` docker start rabbitmq-mgmt `

### To Stop Rabbit MQ Docker
` docker stop rabbitmq-mgmt `


"""
Order JSON Object parsed into ProcessEmailService should follow this format
{
userEmail: String,
userName: String,
orderID: String,
courseName: String,
coursePrice: String,
courseDescription: String
}

Example of Order JSON Object
{
    "userEmail" : "celov54484@gpipes.com",
    "userName" : "celo",
    "orderID" : "4500",
    "courseName" : "Data Structure Algorithms",
    "coursePrice" : "$2000",
    "courseDescription" : "A 3rd semester course at SMU, continues to develop students' understanding of object oriented programming, memory management"
    "classID" : 3,
    "runID": 1,
    "userID": 10,
}
"""