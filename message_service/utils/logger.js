const logger = require("pino");
const dayjs = require("dayjs");

const log = logger({
  transport: {
    target: "pino-pretty",
  },
  timestamp: () => `,"time":"${dayjs().format()}"`,
});

module.exports = log;
