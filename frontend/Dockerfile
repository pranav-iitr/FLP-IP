FROM node:18-alpine

LABEL maintainer="fragment"

WORKDIR /usr/frontend

COPY ./package.json ./package.json


COPY . .

RUN yarn install

RUN yarn build

CMD ["yarn", "start"]