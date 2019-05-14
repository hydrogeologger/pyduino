#!/bin/bash

# connect.sh

# Set up device

exec 9>&2
exec 8> >(
    while [ "$r" != "1" ]; do
        # read input, no field separators or backslash escaping, 1/20th second timeout
        IFS='' read -rt 0.05 line
        r=$?
        # if we have input, print the color change control char and what input we have
        if ! [ "${#line}" = "0" ]; then
            echo -ne "\e[1;33m${line}"
        fi
        # end of line detected, print default color control char and newline
        if [ "$r" = "0" ] ; then
            echo -e "\e[0m"
        fi
        # slow infinite loops on unexpected returns - shouldn't happen
        if ! [ "$r" = "0" ] && ! [ "$r" = "142" ]; then
            sleep 0.05
        fi
    done
)
function undirect(){ exec 1>&9; }
function redirect(){ exec 1>&8; }
trap "redirect;" DEBUG
PROMPT_COMMAND='undirect;'

echo "Starting serial communication with arduino\n"

stty -F /dev/ttyS0 cs8 9600 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts

# Check if error ocurred
if [ "$?" -ne 0 ]; then
    echo "\n\nError ocurred, stty exited $?\n\n"
    exit 1;
fi

echo "Set up serial complete!"
echo "Session begins, type 'exit' to stop"

# Let cat read the device $1 in the background

cat </dev/ttyS0&

# Capture PID of background process so it is possible to terminate it when done
bgPid="$!"


printf "\n"
# Read commands from user, send them to device $1
while [ "$cmd" != "exit" ]
do
   read cmd
   echo -n $cmd > /dev/ttyS0
done

# Terminate background read process
kill "$bgPid"

