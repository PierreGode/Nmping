#!/bin/bash
########################### Start ################################
#                                                                #
#                                                                #
#                                                                #
##################################################################

echo "${MENU}"Checking network"${END}"
yourip=$(ip a | grep '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | grep -v 127 | awk '{print $2}' | cut -d '/' -f1)
speed=$( ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` | grep max | awk '{print$4}' | cut -d '/' -f1)
echo your IP is $yourip
echo "$speed ms"
ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo "Network is working" || echo "NO Network"

