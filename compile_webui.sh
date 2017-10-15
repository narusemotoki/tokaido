#!/bin/sh

sudo docker build -f Dockerfile.webuicompiler -t webcompiler .
sudo docker run -v `pwd`:/srv/tokaido webcompiler
