FROM node:18-alpine AS build
WORKDIR /frontend
COPY . .
RUN npm install && npm run build

FROM nginx:alpine

COPY --from=build /frontend/build /usr/share/nginx/html