#!/bin/bash
########################### Start ################################
#                                                                #
#  ping, insert iplist and check   #
#                                                                #
##################################################################
echo "Type in path or file with IP adresse you wish to check"
read IPlisT
date
cat $IPlisT | while read output
do
    ping "$output" > /dev/null
    if [ $? -eq 0 ]; then
    echo "$output is up" 
    else
    echo "$output is down"
    fi
done

