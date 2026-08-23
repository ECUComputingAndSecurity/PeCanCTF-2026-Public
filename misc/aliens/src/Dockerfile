FROM python:3.14.3-alpine

WORKDIR /app

COPY server.py .
COPY articles ./articles

EXPOSE 119

CMD ["python", "server.py"]