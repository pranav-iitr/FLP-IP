# Use an official Node.js runtime as a base image
FROM node:14

# Set the working directory inside the container
WORKDIR /usr/socket

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install application dependencies
RUN yarn install

# Copy the application code to the working directory
COPY . .


# Specify the command to run your application
CMD ["yarn", "start"]
