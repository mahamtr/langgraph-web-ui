FROM node:18-slim

WORKDIR /app

# Install deps
COPY package.json /app/package.json
RUN npm install

# Copy rest of files
COPY . /app

EXPOSE 5173

CMD ["npm", "run", "dev"]
