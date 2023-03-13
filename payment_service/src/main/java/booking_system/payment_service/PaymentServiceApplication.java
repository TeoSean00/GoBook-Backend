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
		Stripe.apiKey = stripeApiKey;
	}
	public static void main(String[] args) {
		SpringApplication.run(PaymentServiceApplication.class, args);
	}

}
