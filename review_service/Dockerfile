FROM python:3-slim as build
WORKDIR /review_service
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./review.py .
CMD [ "python", "./review.py" ]
