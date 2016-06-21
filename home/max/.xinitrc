#!/bin/bash

date >> /logs/flask_backend_log.txt
python /source/flask_backend.py >> /logs/flask_backend_log.txt &
chromium --kiosk /frontend/index.html &

exec startlxde

