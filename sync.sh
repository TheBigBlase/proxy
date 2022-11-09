#!/bin/bash

LTIME=$(stat -c %Z ./src/*)

while true
do
   ATIME=$(stat -c %Z ./src/*)

   if [[ "$ATIME" != "$LTIME" ]]
   then
       scp -r ./src ubuntu@51.178.85.45:/home/ubuntu/proxy/
       LTIME=$ATIME
   fi
   sleep 1
done
