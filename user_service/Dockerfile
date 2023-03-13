FROM python:3-slim as build
WORKDIR /user_service
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./user.py .
CMD [ "python", "./user.py" ]
