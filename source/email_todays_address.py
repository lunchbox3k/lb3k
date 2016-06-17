import mandrill
import sys


def read_file():
    with open("/restaurants/todays_address.txt", 'r') as F:
	return F.read()


def email_the_address():
    try:
        mandrill_client = mandrill.Mandrill('mXGeLCGXhGCrtiNMXCHCkQ')
        subject_val = "Today's LB3K Address"
        body_val = read_file()
        print(subject_val)
        print(body_val)
        message = {
            'from_name': 'SeamsLessComplicated',
            'from_email': 'SeamsLessComplicated@mail.com',
            'subject': subject_val,
            'to': [{'email': 'mwarner@factset.com',
                    'name': 'Max Warner',
                    'type': 'to'},
                   {'email': 'adsmith@factset.com',
                    'name': 'Adam Smith',
                    'type': 'to'},
                   {'email': 'jpiercy@factset.com',
                    'name': 'Jason Piercy',
                    'type': 'to'}],
            'merge_language': 'mailchimp',
            'text': body_val
        }
        result = mandrill_client.messages.send(message)
        print(result)
        if result[0]['status'] == 'sent' and result[0]['reject_reason'] == None:
            sys.exit(0)
        else:
            sys.exit(1)
    except mandrill.Error as e:
        print("A mandrill error occurred: ", e)
        raise

if __name__ == '__main__':
    email_the_address()
