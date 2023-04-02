FROM python:3-slim as build
WORKDIR /process_booking_service
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./process_booking.py ./amqp_setup.py ./invokes.py .
CMD [ "python", "./process_booking.py" ]
