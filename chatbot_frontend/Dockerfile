# frontend/Dockerfile
FROM node:20 AS build

WORKDIR /chatbot-website

COPY . .

RUN npm install && npm run build

FROM nginx:alpine

COPY --from=build /chatbot-website/build /usr/share/nginx/html
