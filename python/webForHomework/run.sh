#!/bin/sh
if [ -d "all" ];
then 
    echo "yes"
    mkdir all
else
    echo "no"
fi

iptables -I INPUT -p tcp --dport 9020 -j ACCEPT

export PYTHONIOENCODING=utf-8;

nohup python3 ./summitHomework.py &
