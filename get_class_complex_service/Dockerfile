FROM python:3-slim as build
WORKDIR /get_class_complex_service
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./get_class.py .
CMD [ "python", "./get_class.py" ]
