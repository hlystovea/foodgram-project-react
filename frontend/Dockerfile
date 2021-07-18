FROM node:13.12.0-alpine as build
WORKDIR /react
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:latest
COPY --from=build /react/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]