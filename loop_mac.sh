#!/bin/bash

dir="/Users/enriqueramosmunoz/Documents/gitlab/camera"
set -a
. $dir/.env
set +a
echo $CAMERA_KEY
echo $dir
while true; 
  do
  cd $dir
  git pull
  . $dir/install_mac.sh
  for i in `seq 1 600`
  do 
    python3 $dir/send_mac.py
  done
done
