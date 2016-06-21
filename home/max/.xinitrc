#!/bin/bash

date >> /logs/flask_backend_log.txt
python /source/flask_backend.py >> /logs/flask_backend_log.txt &
export CHROME_LOG_FILE=/logs/chrome_log.txt
chromium --kiosk /frontend/index.html --enable-logging --v=1 &

exec startlxde

