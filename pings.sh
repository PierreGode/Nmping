#!/bin/bash
########################### Start ################################
#                                                                #
#   Start ping to google and then send to servers or to loop     #
#                                                                #
##################################################################
start(){
content=$(cat logs/pinglog.log)
if [ $content = 2 ]
then
break;
else
IP='www.google.se'
fping -c1 -t300 $IP 2>/dev/null 1>/dev/null
  if [ "$?" = 0 ]
then
  echo "1" > logs/pinglog.log
servers
else
controll
  fi
fi
}
controll(){
sleep 7
IP='www.google.se'
fping -c1 -t300 $IP 2>/dev/null 1>/dev/null
  if [ "$?" = 0 ]
then
  echo "1" > logs/pinglog.log
servers
else
pico2wave -w logs/ping.wav "Hello technical operations., I have connection troubles" && aplay logs/ping.wav
loop
  fi
}
############################# loop ###############################
#                                                                #
#               Loop loops pings google till success             #
#                                                                #
##################################################################
loop(){
sleep 10
IP='www.google.com'
fping -c1 -t3000 $IP 2>/dev/null 1>/dev/null
if [ "$?" = 0 ]
then
pico2wave -w logs/ping1.wav "hurray. We have network connection again" && aplay logs/ping1.wav 
echo "1" > pinglog.log
else
loop
fi
}
start
