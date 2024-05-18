FROM python:3.8-slim-buster

RUN apt update -y && \
    apt install ffmpeg -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3", "-u" ]

CMD ["src/main.py"]
