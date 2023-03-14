FROM python:3-slim as build
WORKDIR /class_service
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./class.py .
CMD [ "python", "./class.py" ]
