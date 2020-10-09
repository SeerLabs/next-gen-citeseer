FROM node:14.13.1-stretch
EXPOSE 3000
WORKDIR /client
COPY package.json *npm* ./

# Install Node
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt-get install -y nodejs \
  && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg |  apt-key add - \
  && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
  && apt-get update && apt-get install npm \
  && cd /post/frontend \
  && /usr/local/bin/node /client/node_modules/fibers/build \
  && npm install && npm run build
