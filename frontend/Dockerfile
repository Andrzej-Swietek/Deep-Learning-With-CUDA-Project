FROM node:20-alpine

WORKDIR /app

COPY . .

RUN npm install

# Expose the port that Vite uses
EXPOSE 5173

# Start the development server with Vite
CMD ["npm", "run", "dev", "--", "--host", "--port", "5173"]

## Etap 1: Budowanie aplikacji
#FROM node:20-alpine AS build
#
#WORKDIR /app
#
#COPY . .
#
#RUN npm install
#
#RUN npm run build
#
## Etap 2: Serwowanie aplikacji za pomocą lekkiego serwera
#FROM node:20-alpine
#
#WORKDIR /app
#
#COPY --from=build /app/.svelte-kit ./build
#COPY --from=build /app/package.json ./package.json
#COPY --from=build /app/package-lock.json ./package-lock.json
#
#RUN npm install --only=production
#
#RUN npm install vite@latest -g
#
#EXPOSE 5173
#
#CMD ["npm", "run", "preview", "--", "--host", "--port", "5173"]
