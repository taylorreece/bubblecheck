FROM node:current-stretch

RUN npm install -g create-react-app
RUN mkdir /app
WORKDIR /app
ADD ./package.json /app/
ADD ./package-lock.json /app/
ADD ./tsconfig.json /app/
RUN npm install

ENTRYPOINT ["npm", "run", "start"]
