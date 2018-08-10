 #! /usr/bin/env python3

__author__ = "seanwlk"
__copyright__ = "Copyright 2018"
__license__ = "GPL"
__version__ = "2.1"
__maintainer__ = "seanwlk"
__status__ = "Beta"

import sys
import time
import signal
import requests
import json
import getpass

s = requests.Session()

# Login credentials request
email = input("Email: ")
password = getpass.getpass("Password: ")
# Login credentials request

def login():
    # Base header
    payload = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9,it;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'s=dpr=1; amc_lang=en_US; t_0=1; _ym_isad=1',
        'DNT':'1',
        'Host':'auth-ac.my.com',
        'Origin':'https://wf.my.com',
        'Referer':'https://wf.my.com/kiwi',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
        }
    login_data = {
        'email':email,
        'password':password,
        'continue':'https://account.my.com/login_continue/?continue=https%3A%2F%2Faccount.my.com%2Fprofile%2Fuserinfo%2F',
        'failure':'https://account.my.com/login/?continue=https%3A%2F%2Faccount.my.com%2Fprofile%2Fuserinfo%2F',
        'nosavelogin':'0'
        }
    while True:
        try: 
            s.post('https://auth-ac.my.com/auth',headers=payload,data=login_data)
            s.get('https://auth-ac.my.com/sdc?from=https%3A%2F%2Fwf.my.com')
            s.get('https://wf.my.com/')  
            get_token = s.get('https://wf.my.com/minigames/user/info').json()
            s.cookies['mg_token'] = get_token['data']['token']
            s.cookies['cur_language'] = 'en'
        except:
            continue
        break

def get_mg_token():
    get_token = s.get('https://wf.my.com/minigames/user/info').json()
    s.cookies['mg_token'] = get_token['data']['token']

#Class for color and text customization
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def signal_handler(signal, frame):
    print ('\n'+bcolors.WARNING+"K.I.W.I. Crate Manager was interrupted!"+bcolors.ENDC)
    sys.exit(0)

def res_count():
    main_json = s.get("https://wf.my.com/minigames/bp4/craft/user-craft-info").json()
    level1=main_json['data']['user_resources'][0]['amount']
    level2=main_json['data']['user_resources'][1]['amount']
    level3=main_json['data']['user_resources'][2]['amount']
    level4=main_json['data']['user_resources'][3]['amount']
    level5=main_json['data']['user_resources'][4]['amount']
    output = "\033[92m\nCurrent resources\033[0m \nLevel 1: %d | Level 2: %d | Level 3: %d | Level 4: %d | Level 5: %d \n" % (level1,level2,level3,level4,level5)
    return output

print (bcolors.OKGREEN+bcolors.HEADER+"\nK.I.W.I. Weapon Crafting Crate Manager"+bcolors.ENDC)

# LOGIN AND CHECK USER
login()
user_check_json = s.get('https://wf.my.com/minigames/bp4/info/compose?methods=user.info').json()
try:
    print ("Logged in as {}".format(user_check_json['data']['user']['info']['username']))
except KeyError:
    print ("Login failed.")
    sys.exit(0)
# LOGIN AND CHECK USER

signal.signal(signal.SIGINT, signal_handler)
while 1:
    try:
        main_json = s.get("https://wf.my.com/minigames/bp4/craft/user-craft-info").json()
        if len(main_json['data']['user_chests']) != 0:
            for chest in main_json['data']['user_chests']:
                if str(chest['state']) == 'new':
                    get_mg_token()
                    data_start_opening = {
                        'chest_id':chest['id']
                        }
                    req = s.post("https://wf.my.com/minigames/bp4/craft/start",data=data_start_opening)
                    if req['state'] == "Success":
                        print ("New "+chest['type']+" crate available!")
                elif chest['ended_at'] < 0:
                    get_mg_token()
                    data_to_open = {
                        'chest_id':chest['id'],
                        'paid':0
                        }
                    to_open_json = s.post("https://wf.my.com/minigames/bp4/craft/open",data=data_to_open).json()
                    print ('\n'+chest['type']+" crate opening...\n    Content -> Level: "+str(to_open_json['data']['resource']['level'])+" | Amount: "+str(to_open_json['data']['resource']['amount']))
                    #print (res_count()) #Display current resources after each box opened
    except (KeyError,ValueError,TypeError,requests.exceptions.ChunkedEncodingError,json.decoder.JSONDecodeError,requests.exceptions.ConnectionError):
        login()
        pass
    time.sleep(30)

print ("\nUnexpected exit out of the while.")
