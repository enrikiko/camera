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
  . $dir/install.sh
  for i in `seq 1 2`
  do 
    python $dir/send.py
    sleep 1
  done
done
