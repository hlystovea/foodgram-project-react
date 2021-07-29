FROM node:13.12.0-alpine as build
WORKDIR /react
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build