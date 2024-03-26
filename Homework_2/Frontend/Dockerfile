#NEXT APP
FROM node:lts-alpine3.19
WORKDIR /usr/src/app
COPY . .
RUN npm install


RUN npm run build

CMD ["npm", "start"]
