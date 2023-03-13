package booking_system.payment_service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.stripe.Stripe;

import jakarta.annotation.PostConstruct;

@SpringBootApplication
public class PaymentServiceApplication {

	@Value("${stripe.api.key}")
	private String stripeApiKey;

	@PostConstruct
	public void setup(){
		Stripe.apiKey = "sk_test_51MkznJJTqG9NvRuTocMwazTMTEeBy768PQxBvO4Srz98L9TVFOmQu09Q5HXpmuJuPHedPsgfVEQLX3RDMyEtveqE007p8h6WmP";
	}
	public static void main(String[] args) {
		SpringApplication.run(PaymentServiceApplication.class, args);
	}

}
