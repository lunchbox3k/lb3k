from bs4 import BeautifulSoup
import requests
import re
from shutil import copy
import os
import string

def get_lunch_options():
    print("getting lunch options")
    un = 'JPiercy3'
    pw = 'seamslesscomplicated'
    payload = {'username': un, 'password': pw}
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    s = requests.session()
    corp_url = "http://www.seamless.com/corporate/login"
    r = s.get(corp_url, data=payload, headers=headers)
    r2 = s.post('https://www.seamless.com/food-delivery/login.m', headers=headers, data=payload)
    soup = BeautifulSoup(r2.text)
    restaurants = soup.find_all(href=re.compile('groupOrderId'))
    return [''.join(c for c in restaurant.string if ord(c)<128) for restaurant in restaurants if restaurant.string]

def hard_code_names_in_html(names):
    with open("/restaurants/todays_names.txt", 'w') as F:
        F.write('\n'.join(names))
    print("names written in todays_names.txt file")
    first_time_prefix = '<div class="seamless-slide" id="main-slide">\n                            <span class="seamless-text" >'
    all_others_prefix = '<div class="seamless-slide" id="{}">\n                            <span class="seamless-text">'
    suffix = '</span>\n                        </div>'
    spacer = '\n                        '
    replacement_text=""
    for i,name in enumerate(names):
        replacement_text += spacer + all_others_prefix.format(i) + name + suffix
    path_to_customized_file = '/frontend/index.html'
    if os.path.exists(path_to_customized_file):
        os.remove(path_to_customized_file)
    copy('/frontend/index_template.html', path_to_customized_file)
    
    with open (path_to_customized_file, 'r') as myfile:
        data=myfile.read()
        
    data = data.replace('XXX', replacement_text)
    names_array = '["' + '", "'.join(names) + '"]'
    data = data.replace('YYY', names_array)
    zero_array = '[' + ', '.join(['0']*len(names)) + ']'
    data = data.replace('ZZZ', zero_array)
    print("changes made to html in memory")
    with open (path_to_customized_file, 'w') as myfile:
        myfile.write(data)
    print("changes written to new html")
        
def main():
    names = get_lunch_options()
    #names = ["El Ranchito Gourmet Pizza (N Milwaukee)", "Freshii (200 W Monroe)", "Avanti Caffe"]
    print(names)
    hard_code_names_in_html(names)

if __name__ == "__main__":
    main()
