FROM node:18
WORKDIR /CryptoViz_Front
COPY ./ ./
COPY package.json ./
COPY package-lock.json ./
RUN npm i

EXPOSE 8080
ARG VUE_APP_API_URL
ENV VUE_APP_API_URL=$VUE_APP_API_URL
CMD ["npm", "run", "serve"]