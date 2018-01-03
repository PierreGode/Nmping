#!/bin/bash
########################### Start ################################
#       Author: Pierre Goude                                     #
#                                                                #
# Not finished script, its working but it is really just a       #
# dumb thing. unless you want to create a service to log         #
# with it to monitor responsetimes.                              #
# then just remove the #,s below and run it with cron or service #
##################################################################

#dates=$(date +%Y-%m-%d:%H:%M:%S)
#while true
#do
echo "${MENU}"Checking network"${END}"
yourip=$(ip a | grep '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | grep -v 127 | awk '{print $2}' | cut -d '/' -f1)
speed=$( ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` | grep max | awk '{print$4}' | cut -d '/' -f1)
echo your IP is $yourip # $dates | sudo tee -a /var/log/networkping.log
echo "$speed ms" # $dates | sudo tee -a /var/log/networkping.log
#echo "___________________________________" | sudo tee -a /var/log/networkping.log
ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo "Network is working" || echo "NO Network"
#done
