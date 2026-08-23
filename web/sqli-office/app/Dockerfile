# syntax=docker/dockerfile:1.4
FROM python:3.14-alpine AS builder

WORKDIR .

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 80

#Run the app
CMD ["python3", "app.py"]
