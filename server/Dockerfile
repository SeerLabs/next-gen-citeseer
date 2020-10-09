FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /next-gen-seer
WORKDIR /next-gen-seer
ADD . /next-gen-seer/
RUN apt-get update && apt-get install -y \
  libsasl2-dev \
  python3-dev \
  libldap2-dev \
  libssl-dev \
  libcairo2-dev pango1.0-tests \
  libxml2-dev \
  libxmlsec1-dev \
  libxmlsec1-openssl \
  && pip install -r requirements.txt