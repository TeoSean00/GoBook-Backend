const router = require("express").Router();
// not a default export hence {}
const { test, emailTicket } = require("../controller/appController.js");

// HTTP Request
router.post("/user/test", test);
router.post("/product/emailTicket", emailTicket);

module.exports = router;
