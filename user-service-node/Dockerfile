# Tell Docker to use the "node" Docker Image at version "10.15.3"
FROM node:10.15.3
# Create our containers WORKDIR and "node_modules" directory.
# Give the user:group "node" ownership of all files/directories in our containers WORKDIR
# RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app
# Tell our container which directory to use as the WORKDIR
WORKDIR /home/node/app
# Copy over our local version of "package.json" and "package-lock.json" into our container
COPY package*.json ./

COPY app.js .
# Installs our NPM packages from the "package.json" file we moved from local in to our container
RUN npm install
# Exposes the port "3000" from our container
# This is also how we can connect to our container from our host machine (the one you're reading this from now)
EXPOSE 3000

ENTRYPOINT [ "node","app.js" ]
# An array of commands our container needs to run when we start it
# CMD ["node", "run", "start"]