FROM python:latest as build
WORKDIR /consumer_service
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./consumer.py .
CMD [ "python", "./consumer.py" ]