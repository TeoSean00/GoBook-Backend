FROM python:latest as build
WORKDIR /recommendation_service
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./processBookingData.py ./contentBasedFilter.py .
CMD [ "python", "./processBookingData.py" ]