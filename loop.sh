#!/bin/bash

dir=$(pwd)
set -a
. $dir/.env
set +a
echo $CAMERA_KEY
echo $dir
while true; 
  do
  git pull
  for i in `seq 1 5`
  do 
    python $dir/send.sh 
    sleep 1
  done
done
