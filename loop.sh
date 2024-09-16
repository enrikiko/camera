#!/bin/bash

dir="/home/miso/Desktop/camera"
set -a
. $dir/.env
set +a
echo $CAMERA_KEY
echo $dir
while true; 
  do
  git -C $dir pull
  . $dir/install.sh
  for i in `seq 1 2`
  do 
    python $dir/send.py
    sleep 1
  done
done
