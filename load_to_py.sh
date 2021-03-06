#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo "$DIR/pifirestick" 
scp -r "$DIR/pifirestick" pi@192.168.1.26:/home/pi/pi-firestick/
