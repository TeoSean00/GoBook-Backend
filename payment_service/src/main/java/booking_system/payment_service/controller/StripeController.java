package booking_system.payment_service.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
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

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

@RestController
public class StripeController {

    private Logger logger = LoggerFactory.getLogger(StripeController.class);

    private HttpHeaders headers;

    private RestTemplate restTemplate;

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Value("${stripe.webhook.secret}")
    private String endpointSecret;

    public String processing_URL = "http://host.docker.internal:5008/update_payment";

    public StripeController() {
        this.restTemplate = restTemplate();
        headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
    }

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
                HttpEntity<PaymentIntent> request = new HttpEntity<>(paymentIntent, headers);

                ResponseEntity<Object> result = restTemplate.postForEntity(processing_URL, request, Object.class);
                System.out.println(result);
                break;
            case "payment_method.attached":
                PaymentMethod paymentMethod = (PaymentMethod) stripeObject;
                logger.info("payment method attached", paymentMethod);
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
