package booking_system.payment_service.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

import com.stripe.exception.SignatureVerificationException;
import com.stripe.model.Event;
import com.stripe.model.EventDataObjectDeserializer;
import com.stripe.model.PaymentIntent;
import com.stripe.model.PaymentMethod;
import com.stripe.model.StripeObject;
import com.stripe.net.Webhook;

@RestController
public class StripeController {

    private Logger logger = LoggerFactory.getLogger(StripeController.class);

    @Value("${stripe.webhook.secret}")
    private String endpointSecret;

    @PostMapping("/stripe/events")
    public String handleStripeEvent(@RequestBody String payload, @RequestHeader("Stripe-Signature") String sigHeader) {

        if (sigHeader == null) {
            return "";
        }

        Event event;

        try {
            event = Webhook.constructEvent(
                    payload, sigHeader, "whsec_a9ccf263c2ad3b18a0b6071def608dd7a489bc7ee82461e4effbf5d1ad4fb527");
        } catch (SignatureVerificationException e) {
            // Invalid signature

            logger.info("⚠️  Webhook error while validating signature.");
            return "";
        }

        // Deserialize the nested object inside the event
        EventDataObjectDeserializer dataObjectDeserializer = event.getDataObjectDeserializer();
        StripeObject stripeObject = null;
        if (dataObjectDeserializer.getObject().isPresent()) {
            stripeObject = dataObjectDeserializer.getObject().get();
        } else {
            // Deserialization failed, probably due to an API version mismatch.
            // Refer to the Javadoc documentation on `EventDataObjectDeserializer` for
            // instructions on how to handle this case, or return an error here.
        }
        // Handle the event
        switch (event.getType()) {
            case "payment_intent.succeeded":
                PaymentIntent paymentIntent = (PaymentIntent) stripeObject;
                System.out.println("Payment for " + paymentIntent.getAmount() + " succeeded.");
                logger.info("Payment for id={}, {} succeeded", paymentIntent.getId(), paymentIntent.getAmount());
                // Then define and call a method to handle the successful payment intent.
                // handlePaymentIntentSucceeded(paymentIntent);
                
                break;
            case "payment_method.attached":
                PaymentMethod paymentMethod = (PaymentMethod) stripeObject;
                // Then define and call a method to handle the successful attachment of a
                // PaymentMethod.
                // handlePaymentMethodAttached(paymentMethod);
                break;
            default:
                System.out.println("Unhandled event type: " + event.getType());
                break;
        }
        return "";
    };
}
