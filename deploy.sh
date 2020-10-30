#!/bin/bash
docker kill server client > /dev/null 2>&1
docker rm server client > /dev/null 2>&1
docker-compose up -d
