const nodemailer = require("nodemailer");
const Mailgen = require("mailgen");
const logger = require("../utils/logger");
const { EMAIL, PASSWORD } = require("../env.js");
const EmailModel = require("../schema/emailLog.js");
const { getLogger } = require("nodemailer/lib/shared/index.js");
const createPDF = require("../eticket/ticket.js");
const date = require('date-and-time');

// Send mail from testing account
const test = async (req, res) => {
  // testing account
  let testAccount = await nodemailer.createTestAccount();

  // create reusable transporter object using the default SMTP transport
  let transporter = nodemailer.createTransport({
    host: "smtp.ethereal.email",
    port: 587,
    secure: false, // true for 465, false for other ports
    auth: {
      user: testAccount.user, // generated ethereal user
      pass: testAccount.pass, // generated ethereal password
    },
  });

  let message = {
    from: '"Fred Foo 👻" <foo@example.com>', // sender address
    to: "keithloh99@gmail.com, baz@example.com", // list of receivers
    subject: "Hello ✔", // Subject line
    text: "Class Registeration success", // plain text body
    html: "<b>Successfully register for class</b>", // html body
  };

  transporter
    .sendMail(message)
    .then((info) => {
      return res.status(201).json({
        message: "You should receive an email",
        info: info.messageId,
        preview: nodemailer.getTestMessageUrl(info),
      });
    })
    .catch((error) => {
      return res.status(500).json({ message: "Something went wrong" });
    });
};

// Real email sending function
// Changed from req,res to data as it is now called from the queue
const emailTicket = async (data) => {
  const {
    userEmail,
    userName,
    orderID,
    courseName,
    coursePrice,
    courseDescription,
  } = data;

  // No longer taking from request body for object
  // const { userEmail } = req.body;
  // const { userName } = req.body;
  // const { orderID } = req.body;
  // const { courseName } = req.body;
  // const { coursePrice } = req.body;
  // const { courseDescription } = req.body;

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
  const formattedDate = date.format(now, 'MMM DD YYYY');
  console.log(formattedDate);
  let transporter = nodemailer.createTransport(config);

  //! QR CODE NOT NEEDED ANYMORE CALL API TO GET QR CODE
  // Create QR Code Img File
  // QRCode.toFile('./img/qr.png', 'https://www.skillsfuture.gov.sg', {
  //   errorCorrectionLevel: 'H'
  // }, function(err) {
  //   if (err) throw err;
  //   console.log('QR code saved!');
  // });

  // Create QR Code as Binary String
  //  const imgStringPromise = QRCode.toDataURL('https://www.skillsfuture.gov.sg'
  // );
  // const imgString = await imgStringPromise;

  // testing to see if imgString is correct
  // console.log("what is imageString containing?");
  // logger.info(imgString);
  
  // Create of PDF
  const dataObject = 
  {
    "COURSE_NAME":courseName,
    "NAME" : userName,
    "TICKET_NUMBER": orderID,
    "DATE": formattedDate,
    "IMG_SRC": "https://www.skillsfuture.gov.sg"
  };
  // I need the link to the course on the website

  logger.info("starting createPDF Function call ")
  await createPDF(dataObject);
  logger.info("createPDF Function call completed ")

  let MailGenerator = new Mailgen({
    theme: "salted",
    product: {
      name: "Skills Future",
      link: "https://www.skillsfuture.gov.sg",
      // Optional Product Logo
      // logo: 'https://mailgen.js/img/logo.png'
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
      filename: 'eticket.pdf',
      path: 'eticket.pdf',
      contentType: 'application/pdf'
      }
    ]
  };

  // No longer require a res to be sent back as it is now called from the queue
  transporter
    .sendMail(message)
    .then(() => {
      // return res.status(201).json({ msg: "Email sent successfully" });
      logger.info("Email sent successfully");
    })
    .catch((error) => {
      emailObject.success = false;
      logger.info(error);
      // return res.status(500).json({ msg: "Email failed to send" });
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
