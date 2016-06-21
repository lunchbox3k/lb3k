#!/bin/bash

/push_logs.sh

pkill python # maybe "flask_backend"
pkill chromium
/opt/vc/bin/tvservice -o
