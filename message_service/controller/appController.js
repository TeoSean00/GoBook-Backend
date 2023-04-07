const nodemailer = require("nodemailer");
const Mailgen = require("mailgen");
const logger = require("../utils/logger");
const { EMAIL, PASSWORD } = require("../env.js");
const EmailModel = require("../schema/emailLog.js");
const { getLogger } = require("nodemailer/lib/shared/index.js");
const createPDF = require("./ticket.js");
const date = require("date-and-time");

// Testing function to send email to user using POST Request
const test = async (req, res) => {
  // testing account
  const { userEmail } = req.body;
  const { userName } = req.body;
  const { orderID } = req.body;
  const { courseName } = req.body;
  const { coursePrice } = req.body;
  const { courseDescription } = req.body;

  let config = {
    service: "gmail",
    auth: {
      user: EMAIL,
      pass: PASSWORD,
    },
  };

  const emailObject = new EmailModel({
    userEmail: userEmail,
    userName: userName,
    orderID: orderID,
    courseName: courseName,
    coursePrice: coursePrice,
    courseDescription: courseDescription,
    date: Date.now(),
    success: true,
  });
  const now = new Date();
  const formattedDate = date.format(now, "MMM DD YYYY");
  console.log(formattedDate);
  let transporter = nodemailer.createTransport(config);

  // Create of PDF
  const dataObject = {
    COURSE_NAME: courseName,
    NAME: userName,
    TICKET_NUMBER: orderID,
    DATE: formattedDate,
    IMG_SRC: "https://classhero.netlify.app/",
  };
  // I need the link to the course on the website

  logger.info("starting createPDF Function call ");
  await createPDF(dataObject);
  logger.info("createPDF Function call completed ");

  let MailGenerator = new Mailgen({
    theme: "salted",
    product: {
      name: "GoBook",
      link: "https://classhero.netlify.app/",
    },
  });

  let response = {
    body: {
      name: userName,
      intro: ` Ticket is ${orderID}`,
      table: {
        data: [
          {
            item: courseName,
            description: coursePrice,
            price: courseDescription,
          },
        ],
      },
      outro: "Looking forward to do more business with you",
    },
  };

  let mail = MailGenerator.generate(response);

  let message = {
    from: EMAIL,
    to: userEmail,
    subject: `Order #${orderID}`,
    html: mail,
    attachments: [
      {
        filename: "eticket.pdf",
        path: "eticket.pdf",
        contentType: "application/pdf",
      },
    ],
  };

  transporter
    .sendMail(message)
    .then(() => {
      logger.info("Email sent successfully");
      return res.status(201).json({ msg: "Email sent successfully" });
    })
    .catch((error) => {
      emailObject.success = false;
      logger.info(error);
      return res.status(500).json({ msg: "Email failed to send" });
    })
    .finally(async () => {
      logger.info("Logging emailObject to mongo");
      logger.info(`was the email sent successfully? ${emailObject.success}`);
      await emailObject.save();
    });
};

// Send mail to user from AMQP
const emailTicket = async (data) => {
  const {
    userEmail,
    userName,
    orderID,
    courseName,
    coursePrice,
    courseDescription,
  } = data;

  let config = {
    service: "gmail",
    auth: {
      user: EMAIL,
      pass: PASSWORD,
    },
  };

  const emailObject = new EmailModel({
    userEmail: userEmail,
    userName: userName,
    orderID: orderID,
    courseName: courseName,
    coursePrice: coursePrice,
    courseDescription: courseDescription,
    date: Date.now(),
    success: true,
  });
  const now = new Date();
  const formattedDate = date.format(now, "MMM DD YYYY");
  console.log(formattedDate);
  let transporter = nodemailer.createTransport(config);

  const dataObject = {
    COURSE_NAME: courseName,
    NAME: userName,
    TICKET_NUMBER: orderID,
    DATE: formattedDate,
    IMG_SRC: "https://classhero.netlify.app/",
  };

  logger.info("starting createPDF Function call ");
  await createPDF(dataObject);
  logger.info("createPDF Function call completed ");

  let MailGenerator = new Mailgen({
    theme: "salted",
    product: {
      name: "GoBook",
      link: "https://classhero.netlify.app/",
    },
  });

  let response = {
    body: {
      name: userName,
      intro: ` Ticket is ${orderID}`,
      table: {
        data: [
          {
            item: courseName,
            description: courseDescription,
            price: coursePrice,
          },
        ],
      },
      outro: "Looking forward to doing more business with you",
    },
  };

  let mail = MailGenerator.generate(response);
  let message = {
    from: EMAIL,
    to: userEmail,
    subject: `Order #${orderID}`,
    html: mail,
    attachments: [
      {
        filename: "eticket.pdf",
        path: "eticket.pdf",
        contentType: "application/pdf",
      },
    ],
  };

  transporter
    .sendMail(message)
    .then(() => {
      logger.info("Email sent successfully");
    })
    .catch((error) => {
      emailObject.success = false;
      logger.info(error);
    })
    .finally(async () => {
      logger.info("Logging emailObject to mongo");
      logger.info(`was the email sent successfully? ${emailObject.success}`);
      await emailObject.save();
    });
};

module.exports = {
  test,
  emailTicket,
};
