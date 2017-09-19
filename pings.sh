#!/bin/bash
########################### Start ################################
#                                                                #
#                                                                #
#                                                                #
##################################################################

echo "${MENU}"Checking network"${END}"
ifconfig | awk '{print $2}' | grep addr | head -1
speed=$( ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` | grep max | awk '{print$4}' | cut -d '/' -f1)
echo "$speed ms"
ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo "Network is working" || echo "NO Network"

