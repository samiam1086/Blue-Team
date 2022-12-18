#!/bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Enter a list of usernames seperated by commas to whitelist ex kali,test (NOTE SINCE WE ARE RUNNING THIS AS ROOT YOU MUST INCLUDE root IN THE LIST OR YOU GET KICKED OFF THE MACHINE)"

read whitelist # what are the whitelisted account names kali,testuser,etx
tmp="$whitelist"
whitelisted=$(echo $tmp | tr "," "\n") # put each account into an array position

c1=0 # counter
uf=0 # userflag

while true
do
    connected=$(w) # Push the output of w into a variable
    #echo "$connected"
    #echo ""
    IN="$connected" 
    data=$(echo $IN | tr " " "\n") # Parse through the output of w


    for item in $data # run through everything in the $data array
    do
        if [ $c1 -gt 10  ]
        then
            for user in $whitelisted # loop through whitelisted accounts array
            do
                if [ "$user" == "$item" ] # check if $item is in $whitelisted
                then
                    uf=1 # if it is in whitelisted set userflag to 1
                fi
            done
            if [ $uf -eq 0 ] # if userflag is still 0 then whatever is in $item is not in $whitelisted and must due
            then
                sudo killall -u $item 2>/dev/null && echo -e "WARNING: Non-Whitelisted account ${RED}$item${NC} connected and their connection was terminated" # self explanatory
                #echo $item
            fi
            uf=0 # reset userflag
        fi
        let c1++ # counter1 increment
    done
done
