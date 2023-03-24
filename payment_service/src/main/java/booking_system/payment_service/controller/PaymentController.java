package booking_system.payment_service.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;
import com.stripe.Stripe;
import com.stripe.exception.StripeException;
import com.stripe.model.PaymentIntent;
import com.stripe.param.PaymentIntentCreateParams;

@CrossOrigin(origins = "*", maxAge = 3600)
@RestController
public class PaymentController {

    private static Gson gson = new Gson();

    public class CreatePayment {
        private String courseName;
        private Integer coursePrice;
        private String userEmail;
        private Integer course;
        private String orderID;
        private String courseDescription;
        private Integer classID;
        private Integer runID;
        private Integer userID;

        public String getUserEmail() {
            return userEmail;
        }

        public void setUserEmail(String userEmail) {
            this.userEmail = userEmail;
        }

        public Integer getCourse() {
            return course;
        }

        public void setCourse(Integer course) {
            this.course = course;
        }

        public String getOrderID() {
            return orderID;
        }

        public void setOrderID(String orderID) {
            this.orderID = orderID;
        }

        public String getCourseDescription() {
            return courseDescription;
        }

        public void setCourseDescription(String courseDescription) {
            this.courseDescription = courseDescription;
        }

        public Integer getClassID() {
            return classID;
        }

        public void setClassID(Integer classID) {
            this.classID = classID;
        }

        public Integer getRunID() {
            return runID;
        }

        public void setRunID(Integer runID) {
            this.runID = runID;
        }

        public Integer getUserID() {
            return userID;
        }

        public void setUserID(Integer userID) {
            this.userID = userID;
        }

        public String getCourseName() {
            return courseName;
        }

        public void setCourseName(String courseName) {
            this.courseName = courseName;
        }

        public Integer getCoursePrice() {
            return coursePrice;
        }

        public void setCoursePrice(Integer coursePrice) {
            this.coursePrice = coursePrice;
        }

    }

    public class CreatePaymentResponse {
        private String clientSecret;

        public CreatePaymentResponse(String clientSecret) {
            this.clientSecret = clientSecret;
        }
    }

    @PostMapping("/create-payment-intent")
    public String createPaymentIntent(@RequestBody CreatePayment createPayment) throws StripeException {
        System.out.println("createPayment received is");
        System.out.println(createPayment);
        PaymentIntentCreateParams params = PaymentIntentCreateParams.builder()
                .setAmount(createPayment.getCoursePrice() * 100L)
                .setCurrency("sgd")
                .putMetadata("courseDescription", createPayment.getCourseDescription())
                .putMetadata("coursename", createPayment.getCourseName())
                .putMetadata("classId", Integer.toString(createPayment.getClassID()))
                .putMetadata("userEmail", createPayment.getUserEmail())
                .putMetadata("orderID", createPayment.getOrderID())
                .putMetadata("runID", Integer.toString(createPayment.getRunID()))
                .putMetadata("userID", Integer.toString(createPayment.getUserID()))

                .setAutomaticPaymentMethods(
                        PaymentIntentCreateParams.AutomaticPaymentMethods
                                .builder()
                                .setEnabled(true)
                                .build())
                .build();

        // Create a PaymentIntent with the order amount and currency
        PaymentIntent paymentIntent = PaymentIntent.create(params);
        CreatePaymentResponse paymentResponse = new CreatePaymentResponse(paymentIntent.getClientSecret());
        return gson.toJson(paymentResponse);
    };
}
