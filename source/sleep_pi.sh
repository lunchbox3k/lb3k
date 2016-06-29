#!/bin/bash

/source/connect_wifi.sh
/push_logs.sh

pkill python # maybe "flask_backend"
pkill chromium
/opt/vc/bin/tvservice -o
