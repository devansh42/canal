#!/usr/bin/sh
#This scripts agregates all the scripts in this folder
if [ -e final.yaml ]; then
    rm final.yaml

fi

ymls=*yaml
for x in "$ymls"; do
   cat $x >> final.yaml
done
