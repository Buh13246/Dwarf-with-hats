FROM python:3.6.0-alpine
RUN mkdir /app
COPY server.py /app
COPY hats.py /app
WORKDIR /app
EXPOSE 12345
CMD python3 /app/server.py
