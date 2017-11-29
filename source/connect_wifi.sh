

curl http://www.factset.com > /dev/null
curl --ciphers AES256-SHA --data "buttonClicked=4&err_flag=0&err_msg=&info_flag=0&info_msg=&redirect_url=&network_name=Guest802&username=`cat /guest_username.txt`&password=`cat /guest_password.txt`" "https://securewifi.factset.com" > /dev/null
RETVAL=$?

date > /restaurants/todays_address.txt
/sbin/ifconfig >> /restaurants/todays_address.txt

exit $RETVAL
