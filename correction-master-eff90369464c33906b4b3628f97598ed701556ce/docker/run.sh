#!/bin/bash
REPO=docker-reg.emotibot.com.cn:55688
CONTAINER=correction
TAG=$2
DOCKER_IMAGE=$REPO/$CONTAINER:$TAG

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RUNROOT=$DIR/../

echo "RUNROOT : $RUNROOT"

# Load the env file
source $1
if [ $? -ne 0 ]; then
  if [ "$#" -eq 0 ];then
    echo "Usage: $0 <envfile>"
    echo "e.g., $0 dev.env"
  else
    echo "Erorr, can't open envfile: $1"
  fi
  exit 1
else
  echo "# Using envfile: $1"
fi

docker rm -f -v $CONTAINER
cmd="docker run -d --log-opt max-size=10m --log-opt max-file=10 --name $CONTAINER \
    -e CR_DOCKER_PORT=$CR_DOCKER_PORT \
    -m 2048m \
    --restart=on-failure:5 \
    -v /etc/localtime:/etc/localtime \
    -p $CR_DOCKER_PORT:$CR_DOCKER_PORT \
  $DOCKER_IMAGE \
"

echo $cmd
eval $cmd
