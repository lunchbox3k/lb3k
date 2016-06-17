#!/bin/bash

date -s `curl --connect-timeout 20 http://www.timeapi.org/utc/now`

if [ $? != 0 ]; then
  echo "`date`: Couldn't retrieve time" 
else
  echo "`date`: Updated time" 
fi


