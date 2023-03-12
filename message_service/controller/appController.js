const nodemailer = require("nodemailer");
const Mailgen = require("mailgen");

const { EMAIL, PASSWORD } = require("../env.js");
const { Descriptions } = require("antd");
const {successEmailLog, failureEmailLog } = require("./emailLog.js")
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
const emailTicket = (req, res) => {
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

  let transporter = nodemailer.createTransport(config);

  let MailGenerator = new Mailgen({
    theme: "salted",
    product: {
      name: "Skills Future",
      link: "https://mailgen.js/",
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
  };

  transporter
    .sendMail(message)
    .then(() => {

      successEmailLog()
      return res.status(201).json({ msg: "Email sent successfully" });
    })
    .catch((error) => {
      failureEmailLog()
      return res.status(500).json({ msg: "Email failed to send" });
    });

  // res.status(201).json("Get Bill successfully");
};

module.exports = {
  test,
  emailTicket,
};
