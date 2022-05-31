FROM python:3.8-slim-buster

AUTHOR yauri.attamimi@moove.africa
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir data
COPY . .
CMD ["python3", "pipeline_tester.py", "-i", "data/DriverDailyMetrics.xlsx"]