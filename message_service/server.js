const express = require("express");
const logger = require("./utils/logger");
const appRoute = require("./routes/route.js");
const { port } = require("./env.js");
const connectMongo = require("./utils/connectMongo.js");
const amqp = require("amqplib");
const connectQueue = require("./utils/connectAMQP");

const app = express();
const PORT = process.env.PORT || port;
logger.info(port);

app.use(express.json());

// Routes
app.use("/api", appRoute);

app.listen(PORT, async () => {
  logger.info(`Server is running on http://localhost:${PORT}!`);

  await connectMongo();
  await connectQueue();
});
