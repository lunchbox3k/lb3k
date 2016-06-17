#!/bin/bash
/opt/vc/bin/tvservice -p 
pkill python && pkill chromium
pkill x && sudo -u max startx &
