FROM node:12.16.1-buster

COPY . /app

WORKDIR /app

RUN npm i -y --only=prod

VOLUME /app/logs

ENTRYPOINT ["node"]

CMD ["."]
