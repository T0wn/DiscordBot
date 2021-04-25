FROM python:3.9-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

VOLUME /app/logs

ENTRYPOINT ["python3"]

CMD ["main.py"]
