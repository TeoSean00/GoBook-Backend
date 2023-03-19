const router = require("express").Router();
// not a default export hence {}
const { test, emailTicket } = require("../controller/appController.js");

// HTTP Request
router.post("/user/test", test);

// Commented out email ticket as it is no longer a HTTP request but called via queue
// router.post("/product/emailTicket", emailTicket);

module.exports = router;
