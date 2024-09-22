# Stage 1: Build the app
FROM node:20.12.0

# Set working directory inside the container
WORKDIR /app

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Install dependencies
RUN npm install

# Install dependencies
RUN npm install
RUN npm install -g @vue/cli-service

# Expose port 8080 to the outside world
EXPOSE 5143

# Run the application in development mode
CMD ["npm", "run", "dev"]
