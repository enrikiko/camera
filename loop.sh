#!/bin/bash

dir="home/miso/Desktop/camera"
cd $dir
set -a
. .env
set +a
echo $CAMERA_KEY
echo $dir
while true; 
  do
  
  git pull
  . install.sh
  for i in `seq 1 2`
  do 
    python send.py
    sleep 1
  done
done
