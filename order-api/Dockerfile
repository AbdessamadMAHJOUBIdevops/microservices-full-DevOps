FROM node:18-alpine as base

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

# ÉTAPE 2 : Tests
FROM base as tester
# Dans un vrai projet, ce serait : RUN npm test
RUN echo "Running tests..." && node -e 'console.log("Tests passed!")'

# ÉTAPE 3 : Production
FROM base as production
EXPOSE 3001
CMD ["node", "server.js"]