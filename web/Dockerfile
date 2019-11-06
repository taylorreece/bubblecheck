FROM node:current-alpine

RUN npm install -g create-react-app
RUN mkdir /app
WORKDIR /app
ADD ./package.json /app/
ADD ./public/ /app/public/
RUN npm install
RUN npm audit fix

ENTRYPOINT ["npm", "run", "start"]
