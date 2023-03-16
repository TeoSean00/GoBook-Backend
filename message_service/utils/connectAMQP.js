const amqp = require("amqplib");
const logger = require("./logger");
const { rabbitMQ, queueName } = require("../env.js");
const { emailTicket } = require("../controller/appController.js");

var channel, connection;

async function connectQueue() {
  try {
    connection = await amqp.connect(rabbitMQ);
    channel = await connection.createChannel();
    logger.info("RabbitMQ connected");

    await channel.assertQueue(queueName);
    logger.info(queueName);
    channel.consume(queueName, (data) => {
      logger.info("Received data from queue");

      logger.info(`${Buffer.from(data.content)}`);

      const parsedData = JSON.parse(data.content.toString());
      // Call the function emailTicket
      emailTicket(parsedData);
      // If order object is correct
      channel.ack(data);
    });
  } catch (error) {
    logger.error("Could not connect to RabbitMQ");
    logger.error(error);
    process.exit(1);
  }
}

module.exports = connectQueue;
