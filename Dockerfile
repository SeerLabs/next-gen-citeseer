FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /next-gen-seer
WORKDIR /next-gen-seer
ADD . /next-gen-seer/
RUN cd server \
  && apt-get update && apt-get install -y \
  libsasl2-dev \
  python3-dev \
  libldap2-dev \
  libssl-dev \
  libcairo2-dev pango1.0-tests \
  libxml2-dev \
  libxmlsec1-dev \
  libxmlsec1-openssl \
  && pip install -r requirements.txt

# Install Node
# RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
#  && apt-get install -y nodejs \
#  && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg |  apt-key add - \
#  && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
#  && apt-get update && apt-get install npm \
#  && cd /next-gen-seer/client \
#  && npm install && npm run build

#WORKDIR /next-gen-seer/backend
#RUN python app/setup.py install
