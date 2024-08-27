# FROM node:18
# WORKDIR /front-react
# COPY package.json ./
# COPY ./ ./
# RUN rm -rf package-lock.json
# RUN npm i
# EXPOSE 3000
# ARG REACT_APP_API_URL
# ENV REACT_APP_API_URL=$REACT_APP_API_URL
# CMD ["npm", "start"]
FROM node:18
WORKDIR /front-react
COPY ./ ./
COPY package*.json ./
RUN npm install
EXPOSE 3000
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL
WORKDIR /front-react
CMD ["npm", "start"]