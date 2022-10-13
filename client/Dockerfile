FROM node:12.19.0

ENV APP_ROOT /src

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}
ADD . ${APP_ROOT}

RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get update && apt-get install -y nodejs

RUN npm install
RUN npm run build

ENV NODE_OPTIONS "--max-old-space-size=8192"
ENV HOST 0.0.0.0
EXPOSE 3000
CMD npm run dev
