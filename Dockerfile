FROM python:3.8-slim-buster

RUN apt update -y && \
    apt install ffmpeg -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

WORKDIR /app/dictator_bot

ENTRYPOINT [ "python3", "-u" ]

CMD ["__main__.py"]