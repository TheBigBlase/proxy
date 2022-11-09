#!/bin/bash

LTIME=$(stat -c %Z ./src/*)

while true
do
   ATIME=$(stat -c %Z ./src/*)

   if [[ "$ATIME" != "$LTIME" ]]
   then
       python3 main.py --server
       LTIME=$ATIME
   fi
   sleep 1
done
