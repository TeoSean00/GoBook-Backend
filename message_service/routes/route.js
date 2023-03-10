const router = require("express").Router();
// not a default export hence {}
const { signup, getBill } = require("../controller/appController.js");

// HTTP Request
router.post("/user/signup", signup);
router.post("/product/getbill", getBill);

module.exports = router;
