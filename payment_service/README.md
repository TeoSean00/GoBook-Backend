
## Set up Stripe CLI on Docker
### For Mac/Linux
```
docker run --rm --entrypoint /bin/sh -it stripe/stripe-cli:latest
$ stripe login 
$ stripe listen --forward-to host.docker.internal:8080/stripe/events
```
### For Windows
```
docker run --rm --entrypoint /bin/sh -it stripe/stripe-cli:latest
stripe login 
stripe listen --forward-to host.docker.internal:8080/stripe/events
```