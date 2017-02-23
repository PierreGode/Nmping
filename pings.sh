#!/bin/bash
########################### Start ################################
#                                                                #
#     create ip.lst and add a list of ip adresses to check       #
#                                                                #
##################################################################

cat ip.lst | while read output
do
    ping -c 1 "$output" > /dev/null
    if [ $? -eq 0 ]; then
    echo "$output is up" 
    else
    echo "$output is down"
    fi
done

