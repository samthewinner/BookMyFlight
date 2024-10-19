# Use the official Node.js image
FROM node:20-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (if available) into the container
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy the rest of the application code into the container
COPY . . 

# Expose the application port (adjust according to your app)
EXPOSE 3000

# Start the application
CMD ["node", "index.js"]
