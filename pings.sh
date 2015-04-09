#!/bin/bash
########################### Start ################################
#                                                                #
#   Start pings google and the sent to servers och to loop       #
#                                                                #
##################################################################
start(){
content=$(cat logs/pinglog.log)
if [ $content = 2 ]
then
break
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
############################# Servers ############################
#                                                                #
#               servers checks if servers are alive              #
#                                                                #
##################################################################
servers(){
contentmap=`nmap -Pn 0.0.0.0 | grep "443" | cut -d '/' -f1` 
contentmap1=`nmap -Pn 0.0.0.0 | grep "113" | cut -d '/' -f1` 
contentmap2=`nmap -Pn 0.0.0.0 | grep "443" | cut -d '/' -f1` 
tcp="443"
tcp2="113"
contentsrv=$(cat logs/pinglogserv.log)
if [ "$contentsrv" = "2" ]
then
break
else
  if [ "$contentmap" = "$tcp" ]
  then
  echo "1" > logs/pinglogserv.log
  latency=`nmap -Pn 0.0.0.0 | grep "latency" | cut -d '(' -f2 | cut -d 's' -f1`
    if [ $latency > "1.000" ]
    then echo "" & >/dev/null
    else pico2wave -w ping.wav "Hello technical operations,. the latency of server 9 is, $latency" && aplay ping.wav
    fi
  else
  pico2wave -w logs/ping3.wav "Hello technical operations. I belive, that the Adtoox server9, has connection troubles. Host seems to have problems" && aplay logs/ping3.wav
  echo "2" > logs/pinglogserv.log
      if [ "$contentmap1" = "$tcp1" ]
      then
      pico2wave -w logs/ping4.wav "But, Adtoox server 10 is up" && aplay logs/ping4.wav
      break
      else
      pico2wave -w logs/ping5.wav "Also, Adtoox server 10 seems to be down" && aplay logs/ping5.wav
    fi
  fi
fi
############################# Sites ##############################
#                                                                #
#               sites checks if certain sites are up             #
#                                                                #
##################################################################
}
sites(){
echo ""
}
start