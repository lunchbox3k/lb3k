import requests
import json
import sys
import mailgun_api

def pretty_info(info):
    return 'Restaurant: {}\n\tAverage: {}\n\tEarliest: {}\n\tLatest: {}\n\tMost Recent: {}\n\tNumber of Deliveries: {}'.format(info['restaurant'], info['average'], info['earliest'], info['latest'], info['most_recent'], info['number_deliveries'])


def get_msg_body():
    body_val = "WARNING: this email does not exist. These are not the stats you're looking for.\n\n"
    body_val += "http://www.seamless.com/corporate/login\n\n"
    body_val += "Today's Scraped Lunch Options:\n"
    restaurants = ""
    stats_data = {}
    with open("/restaurants/todays_names.txt", 'r') as F:
        restaurants = F.read().splitlines()
    with open("/source/rest_stats.json", 'r') as F:
        stats_data.update(json.load(F))
    if not restaurants:
        body_val = "There seems to be no parsed restaurants, whoops"
    else:
        for restaurant in restaurants:
            rest_data = stats_data.get(restaurant)
            if not rest_data:
                rest_data = "Restaurant: " + restaurant + "\n\tNo Data found"
            else:
                if 'most_recent' not in rest_data:
                    rest_data['most_recent'] = "N/A...for now"
                rest_data.update({'restaurant': restaurant})
                rest_data = pretty_info(rest_data)
            body_val += "\n"+rest_data

    return body_val


def email_the_address():
    result = requests.post("https://api.mailgun.net/v3/pretos.com/messages", auth=("api", mailgun_api.get_key()), data={"from": "LunchBox3000@pretos.com", "to": "adsmith@factset.com", "subject": "LB3K scrape results", "text": get_msg_body()}, verify=False)
    if result.status_code != 200:
        sys.exit(1)

if __name__ == '__main__':
    email_the_address()
