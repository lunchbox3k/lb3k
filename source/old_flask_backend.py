from flask import Flask
import mandrill


app = Flask(__name__)
SERVER_PORT = 11011

restaurants = []
email_has_been_sent = []


@app.route('/arrived/<int:index>', methods=['POST'])
def food_has_arrived(index):
    if not email_has_been_sent[index]:
        email_has_been_sent[index] = 1
        email_notification_for(restaurants[index])
	print(restaurants[index])


def init():
    global restaurants
    global email_has_been_sent
    with open("/restaurants/todays_names.txt", 'r') as F:
        restaurants = F.read().splitlines()
    email_has_been_sent = [0]*len(restaurants)


def email_notification_for(restaurant_arrived_name):
    try:
        mandrill_client = mandrill.Mandrill('mXGeLCGXhGCrtiNMXCHCkQ')
        subject_val = restaurant_arrived_name + ' is here!!'
        print (subject_val)
        print (restaurant_arrived_name)
        message = {
            'from_name': 'SeamsLessComplicated',
            'from_email': 'SeamsLessComplicated@mail.com',
            'subject': subject_val,
            'to': [{'email': 'mwarner@factset.com',
                    'name': 'Max Warner',
                    'type': 'to'}],
            'merge_language': 'mailchimp'
        }
        result = mandrill_client.messages.send(message)
        print(result)
    except mandrill.Error as e:
        print("A mandrill error occurred: ", e)
        raise


if __name__ == '__main__':
    init()
    app.run("localhost", SERVER_PORT, debug=False)
