#!/bin/bash
########################### Pings ################################
#       Author: Pierre Goude                                     #
#                                                                #
# Not finished script, its working but it is really just a       #
# dumb thing. unless you want to create a service to log,        #
# to monitor responsetimes.                                      #
# then just run it with cron or service                          #
##################################################################

while true
do
dates=$(date +%m-%d" "%H:%M:%S)
echo "${MENU}"Checking network"${END}"
yourip=$(ip a | grep '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | grep -v 127 | awk '{print $2}' | cut -d '/' -f1 | head -1)
speed=$( ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` | grep max | awk '{print$4}' | cut -d '/' -f1)
echo your IP is $yourip | sudo tee -a /var/log/networkping.log
echo "$speed ms"  $dates | sudo tee -a /var/log/networkping.log
echo "___________________________________" | sudo tee -a /var/log/networkping.log
ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo "Network is working" || echo "NO Network"
sleep 1
done
