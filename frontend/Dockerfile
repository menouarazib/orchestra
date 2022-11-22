# Use a Node 16 base image
FROM node:16-alpine 

#Set working directory
WORKDIR /orchestra/frontend

# Copy Package.json files
COPY package.json package.json
COPY package-lock.json package-lock.json

# Update NPM
RUN npm install -g npm
# Install node modules
RUN npm install

# Copy src and public folders
COPY public/ public
COPY src/ src

# Start server
CMD ["npm", "start"]


