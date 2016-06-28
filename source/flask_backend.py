from flask import Flask
import requests
import time
import json
import datetime
from subprocess import call


app = Flask(__name__)
SERVER_PORT = 11011

restaurants = []
email_has_been_sent = []

BACKEND_LOG = '/logs/backend_log.txt'


@app.route('/arrived/<int:index>', methods=['POST'])
def food_has_arrived(index):
    restaurant = restaurants[index]
    write_log('Recieved request for index {}, restaurant {}'.format(index, restaurant))
    if not email_has_been_sent[index]:
        write_log('Email has not been sent for restaurant {}'.format(restaurant))
        email_has_been_sent[index] = 1
        email_notification_for(restaurant)
    else:
        write_log('Email has already been sent for restaurant {}'.format(restaurant))


def init():
    global restaurants
    global email_has_been_sent
    with open("/restaurants/todays_names.txt", 'r') as F:
        restaurants = F.read().splitlines()
    email_has_been_sent = [0]*len(restaurants)
    with open(BACKEND_LOG, 'w') as f:
        f.write('')
    write_log('Today\'s restaurant list is {}'.format(restaurants))


def write_log(log):
    with open(BACKEND_LOG, 'a') as f:
        f.write(str(datetime.datetime.now()) + ': ' + log + '\n')


def email_notification_for(restaurant_arrived_name):
    #try:
    subject_val = restaurant_arrived_name + ' is here!!'
    print (subject_val)
    # body = pretty_info(write_rest_stats(restaurant_arrived_name))
    # print (body)
    status = 0
    attempt = 1
    while status != 200 and attempt <= 5:
        write_log('Sending request to mailgun for restaurant {}'.format(restaurant_arrived_name))
        try:
            result = requests.post("https://api.mailgun.net/v3/sandbox92d50346bad74139acc91c33ac2c50b3.mailgun.org/messages", auth=("api", "key-42e3d9f10b9b041a11918b0aa7dd620d"), data={"from": "LunchBox3000@hotlunch.com", "to": "mwarner@factset.com", "subject": subject_val, "text": " "})
        except Exception as e:
            write_log('Request failed with message {}'.format(e))
            attempt += 1
            call("/source/connect_wifi.sh", shell=True)
            time.sleep(2 ** attempt)
            continue
        # print(result)
        status = result.status_code
        write_log('Request returned {} status code for restaurant {}'.format(status, restaurant_arrived_name))
        attempt += 1
    if status != 200:
        write_log('Out of retry attempts for restaurant {}'.format(restaurant_arrived_name))
    else:
        write_log('Request successfully sent for restaurant {}'.format(restaurant_arrived_name))
    #if result.status_code != 200:
        #raise Exception
    #except mandrill.Error as e:
        #print("A mandrill error occurred: ", e)
        #raise


def write_rest_stats(restaurant):
    file_data = {}
    with open('/source/rest_stats.json', 'r') as file:
        file_data.update(json.load(file))
        rest_data = file_data.get(restaurant)
        current_time = time.localtime()
        print(current_time)
        if not rest_data:
            rest_data = {'earliest': time.strftime("%H:%M", current_time),
                         'average': time.strftime("%H:%M", current_time),
                         'latest': time.strftime("%H:%M", current_time),
                         'most_recent': time.strftime("%H:%M", current_time),
                         'number_deliveries': 1}
        else:
            earliest = time.strptime(rest_data['earliest'], "%H:%M")
            latest = time.strptime(rest_data['latest'], "%H:%M")
            average = time.strptime(rest_data['average'], "%H:%M")
            number_deliveries = rest_data['number_deliveries'] + 1

            if current_time.tm_hour < earliest.tm_hour or (current_time.tm_hour <= earliest.tm_hour and current_time.tm_min < earliest.tm_min):
                rest_data['earliest'] = time.strftime("%H:%M", current_time)
            elif current_time.tm_hour > latest.tm_hour or (current_time.tm_hour >= latest.tm_hour and current_time.tm_min > latest.tm_min):
                rest_data['latest'] = time.strftime("%H:%M", current_time)
            #if current_time.tm_hour <= earliest.tm_hour and current_time.tm_min < earliest.tm_min:
            #    rest_data['earliest'] = time.strftime("%H:%M", current_time)
            #elif current_time.tm_hour >= latest.tm_hour and current_time.tm_min > latest.tm_min:
            #    rest_data['latest'] = time.strftime("%H:%M", current_time)

            average_sum = average.tm_hour * 60 + average.tm_min
            current_sum = current_time.tm_hour * 60 + current_time.tm_min
            average_sum = (average_sum * (number_deliveries - 1) + current_sum) / number_deliveries
            average = time.strptime('{}:{}'.format(int(average_sum / 60), int(average_sum % 60)), "%H:%M")
            
            rest_data['most_recent'] = time.strftime("%H:%M", current_time)
            rest_data['number_deliveries'] = number_deliveries
            rest_data['average'] = time.strftime("%H:%M", average)
        file_data.update({restaurant: rest_data})
    with open('/source/rest_stats.json', 'w') as file:
        file.write(json.dumps(file_data))
    rest_data.update({'restaurant': restaurant})
    print('json stats updated')
    return rest_data


def pretty_info(info):
    return 'Restaurant: {}\nAverage: {}\nEarliest: {}\nLatest: {}\nMost Recent: {}\nNumber of Deliveries: {}'.format(info.get('restaurant', 'na'), info.get('average', 'na'), info.get('earliest', 'na'), info.get('latest', 'na'), info.get('most_recent', 'na'), info.get('number_deliveries', 'na'))


if __name__ == '__main__':
    init()
    app.run("localhost", SERVER_PORT, debug=False)
