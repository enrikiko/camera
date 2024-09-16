#!/bin/bash

dir=$(pwd)
set -a
. $dir/.env
set +a
while true; 
  do
  git pull
  for i in `seq 1 100`
  do 
    python $dir/send.sh 
    sleep 1
  done
done
