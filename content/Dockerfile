
FROM node

WORKDIR content

COPY ./package.json .

RUN npm install

COPY . .

CMD ["node", "interface.js"]
