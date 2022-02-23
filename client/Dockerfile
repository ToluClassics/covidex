FROM node:17.4.0

WORKDIR /client
COPY . /client/

RUN yarn install

EXPOSE 3000

CMD ["yarn", "start"]