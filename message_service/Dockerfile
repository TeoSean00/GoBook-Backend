# Use the official Node.js image as the base image
FROM node:current-alpine

# manually installing chrome
RUN apk add chromium

# skips puppeteer installing chrome and points to correct binary
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser


# Set the working directory for the app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install the app's dependencies
RUN npm install
# RUN npm ci --only=production

# Copy the rest of the app's source code to the working directory
COPY . .

# Expose the port on which the app runs (replace 3000 with the actual port if different)
EXPOSE 4006

# Start the app
CMD ["npm", "start"]

# 