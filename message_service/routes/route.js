const router = require("express").Router();
const { test } = require("../controller/appController.js");

// HTTP Request
router.post("/test", test);

module.exports = router;
