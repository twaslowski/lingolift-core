FROM node:16-alpine AS build

ARG ENVIRONMENT
WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build -- --configuration $ENVIRONMENT

# Serve Application using Nginx Server
FROM nginx:alpine

COPY --from=build /app/dist/lingolift/ /usr/share/nginx/html

EXPOSE 80