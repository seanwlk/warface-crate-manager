 #!/usr/bin/env python3

__author__ = "seanwlk"
__copyright__ = "Copyright 2019"
__license__ = "GPL"
__version__ = "3.1"

import sys, os
import time
import signal
import requests
import json
import getpass
import steam.webauth as wa
from collections import OrderedDict
from io import StringIO
import lxml.html

s = requests.Session()

if os.path.isfile('./creds.json'):
    with open('creds.json','r') as json_file:
        CREDS = json.load(json_file)
    is_Steam = CREDS['is_Steam']
    email = CREDS['email']
    password = CREDS['password']    
else:
    while True:
        platform = input("Which platform are you using? \n 1. My.com \n 2. Steam \n 3. Mail.ru    Choice:")
        if platform.lower()=='1':
            is_Steam=1
        elif platform.lower()=='2':
            is_Steam=2
        elif platform.lower()=='3':
            is_Steam=3
        else:
            continue
        break
    # Login credentials request
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    CREDS = {}
    CREDS['is_Steam'] = is_Steam
    CREDS['email'] = email
    CREDS['password'] = password 
    with open('creds.json','w') as json_file:
        json.dump(CREDS, json_file, indent=4, sort_keys=True)
    # Login credentials request

def steam_login():
    # Steam login function by sumfun4WF
    user = wa.WebAuth(email, password)
    try:
        user.login()
    except wa.CaptchaRequired:
        print("Please complete the captcha: "+user.captcha_url)
        captcha_code=input("Please input the captcha response code: ")
        user.login(captcha=captcha_code)
    except wa.EmailCodeRequired:
        email_code=input("Please input the email verification code: ")
        user.login(email_code=email_code)
    except wa.TwoFactorCodeRequired:
        tfa_code=input("Please input the 2FA code: ")
        user.login(twofactor_code=tfa_code)
    # Copy cookies to session
    s.cookies.update(user.session.cookies)
    while True:
        try:
            entrance=s.get('https://auth-ac.my.com/social/steam?continue=https://account.my.com/social_back/?continue=https://wf.my.com/en/&failure=https://account.my.com/social_back/?soc_error=1&continue=https://wf.my.com/en/')
            openid_login={}
            html = StringIO(entrance.content.decode())
            tree = lxml.html.parse(html)
            root = tree.getroot()
            for form in root.xpath('//form[@name="loginForm"]'):
                for field in form.getchildren():
                    if 'name' in field.keys():
                        openid_login[field.get('name')]=field.get('value')
            s.headers.update({'referer': entrance.url})
            steam_redir=s.post('https://steamcommunity.com/openid/login', data=openid_login)
            s.get('https://auth-ac.my.com/sdc?from=https%3A%2F%2Fwf.my.com')
            get_token = s.get('https://wf.my.com/minigames/user/info').json()
            s.cookies['mg_token'] = get_token['data']['token']
            s.cookies['cur_language'] = 'en'
        except:
            continue
        break

def mycom_login():
    payload = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9,it;q=0.8',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'s=dpr=1; amc_lang=en_US; t_0=1; _ym_isad=1',
        'DNT':'1',
        'Origin':'https://wf.my.com',
        'Referer':'https://wf.my.com/battlepass',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
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

def mailru_login():
    # <3 Harmdhast
    payload = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9,it;q=0.8',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'s=dpr=1; amc_lang=en_US; t_0=1; _ym_isad=1',
        'DNT':'1',
        'Origin':'https://wf.mail.ru',
        'Referer':'https://wf.mail.ru/battlepass',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
    s.get('https://auth.mail.ru/cgi-bin/auth?Login={mail}&Password={pwd}&FakeAuthPage=https%3A%2F%2Fwf.mail.ru%2Fauth'.format(mail=email,pwd=password))

def login():
    global base_url
    if is_Steam == 1:
        base_url = "wf.my.com"
        mycom_login()
    elif is_Steam == 2:
        base_url = "wf.my.com"
        steam_login()
    elif is_Steam == 3:
        base_url = "wf.mail.ru"
        mailru_login()

def get_mg_token():
    get_token = s.get('https://{}/minigames/user/info'.format(base_url)).json()
    s.cookies['mg_token'] = get_token['data']['token']

def signal_handler(signal, frame):
    print ("\n\033[93mWarface Crate Manager was interrupted!\033[0m")
    sys.exit(0)

print ("\n\033[95mWarface Crate Manager\033[0m")

# LOGIN AND CHECK USER
login()
user_check_json = s.get('https://{}/minigames/bp/user-info'.format(base_url)).json()
try:
    print ("Logged in as {}".format(user_check_json['data']['username']))
except KeyError:
    print ("Login failed.")
    sys.exit(0)
# LOGIN AND CHECK USER

signal.signal(signal.SIGINT, signal_handler)
while 1:
    try:
        main_json = s.get("https://{}/minigames/craft/api/user-info".format(base_url)).json()
        if len(main_json['data']['user_chests']) != 0:
            for chest in main_json['data']['user_chests']:
                if str(chest['state']) == 'new':
                    get_mg_token()
                    url = "https://{}/minigames/craft/api/start".format(base_url)
                    data_start_opening = {
                        'chest_id':chest['id']
                        }
                    req = s.post(url,data=data_start_opening).json()
                    if req['state'] == "Success":
                        print ("New {chest_type} crate available! {start_result} opening, ID: {chestid}".format(chest_type=chest['type'],start_result=req['state'],chestid=req['data']['id']))
                elif chest['ended_at'] < 0:
                    get_mg_token()
                    data_to_open = {
                        'chest_id':chest['id'],
                        'paid':0
                        }
                    url = "https://{}/minigames/craft/api/open".format(base_url)
                    req = s.post(url,data=data_to_open)
                    to_open_json = json.loads(req.text)
                    print ("\n{chest_type} crate opening...\n    Content -> Level: {level} | Amount: {amount}".format(chest_type=chest['type'],level=to_open_json['data']['resource']['level'],amount=to_open_json['data']['resource']['amount']))
    except (KeyError,ValueError,TypeError,requests.exceptions.ChunkedEncodingError,json.decoder.JSONDecodeError,requests.exceptions.ConnectionError):
        login()
        pass
    time.sleep(30)

print ("\nUnexpected exit out of the while.")
