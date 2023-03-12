const mongoose = require("mongoose");

const emailLogSchema = new mongoose.Schema({
  userEmail: { type: String, required: true },
  userName: { type: String, required: true },
  orderID: { type: String, unique: true },
  courseName: { type: String, required: true },
  coursePrice: { type: String, required: true },
  courseDescription: String,
  date: { type: Date, default: Date.now },
  success: Boolean,
});

const EmailModel = mongoose.model("emaillog", emailLogSchema);

module.exports = EmailModel;