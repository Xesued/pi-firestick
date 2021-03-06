#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo "$DIR" 
scp -r "$DIR" pi@192.168.1.26:/home/pi/
