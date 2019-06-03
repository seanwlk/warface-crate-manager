 #!/usr/bin/env python3

__author__ = "seanwlk"
__copyright__ = "Copyright 2019"
__license__ = "GPL"
__version__ = "1.4"

import sys, os
import datetime
import requests
import json
import steam.webauth as wa
from collections import OrderedDict
from io import StringIO
import lxml.html
from tkinter import * 
from tkinter import simpledialog,messagebox

s = requests.Session()

def check_for_updates(silent=False):
    def latest_ver():
        ver = requests.get("https://api.github.com/repos/seanwlk/warface-crate-manager/releases/latest").json()
        return ver['tag_name']
    print("Looking for udpates")
    if __version__ != latest_ver():
        messagebox.showwarning("New version available!","You are currently running a different version than the latest release available. Please update.")
    else:
        if not silent:
            messagebox.showinfo("No updates available","You are currently running the latest version of the project.")

def resources():
    print("Opening available resources window")
    resources_window = Tk() 
    resources_window.title("Resources")
    resources_window.resizable(False, False)
    resources_window.geometry("300x300")
    main_json = s.get("https://wf.my.com/minigames/craft/api/user-info").json()
    Label(resources_window, text="Current Resources").grid(row=0,column=2,sticky = W)
    level1=main_json['data']['user_resources'][0]['amount']
    level2=main_json['data']['user_resources'][1]['amount']
    level3=main_json['data']['user_resources'][2]['amount']
    level4=main_json['data']['user_resources'][3]['amount']
    level5=main_json['data']['user_resources'][4]['amount']
    Label(resources_window, text="Level 1: {}".format(level1)).grid(row=1,column=2,sticky = W)
    Label(resources_window, text="Level 2: {}".format(level2)).grid(row=2,column=2,sticky = W)
    Label(resources_window, text="Level 3: {}".format(level3)).grid(row=3,column=2,sticky = W)
    Label(resources_window, text="Level 4: {}".format(level4)).grid(row=4,column=2,sticky = W)
    Label(resources_window, text="Level 5: {}".format(level5)).grid(row=5,column=2,sticky = W)
    Label(resources_window).grid(row=6,column=2)
    Label(resources_window, text="If all converted").grid(row=7,column=2,sticky = W)
    Label(resources_window, text="Level 1: {}".format(level1%50)).grid(row=8,column=2,sticky = W)
    level2 = level2 + int(level1/50)
    Label(resources_window, text="Level 2: {}".format(level2%50)).grid(row=9,column=2,sticky = W)
    level3 = level3 + int(level2/50)
    Label(resources_window, text="Level 3: {}".format(level3%35)).grid(row=10,column=2,sticky = W)
    level4 = level4 + int(level3/35)
    Label(resources_window, text="Level 4: {}".format(level4%25)).grid(row=11,column=2,sticky = W)
    level5 = level5 + int(level4/25)
    Label(resources_window, text="Level 5: {}".format(level5)).grid(row=12,column=2,sticky = W)
    
    resources_window.mainloop()
    
def crate_date(end_at):
    if end_at > 0:
        return str(datetime.timedelta(seconds=end_at))
    else:
        return "Crate Open"

def crates():
    print("Opening available crates window")
    crates_window = Tk() 
    crates_window.title("Crates")
    crates_window.resizable(False, False)
    crates_window.geometry("300x200")
    main_json = s.get("https://wf.my.com/minigames/craft/api/user-info").json()
    for index,crate in enumerate(main_json['data']['user_chests']):
       Label(crates_window, text="{type} chest - Opens in {opens}".format(type=crate['type'],opens=crate_date(crate['ended_at']))).grid(row=index,column=0,sticky = W) 
    crates_window.mainloop()

def main_app():
    check_for_updates(silent=True)
    def append_out_text(text):
        out_text.configure(state='normal')
        out_text.insert(END,"\n{}".format(text))
        out_text.configure(state='disabled')
    def check_crates():
        main_json = s.get("https://wf.my.com/minigames/craft/api/user-info").json()
        if len(main_json['data']['user_chests']) != 0:
            for chest in main_json['data']['user_chests']:
                if str(chest['state']) == 'new':
                    get_mg_token()
                    url = "https://wf.my.com/minigames/craft/api/start"
                    data_start_opening = {
                        'chest_id':chest['id']
                        }
                    req = s.post(url,data=data_start_opening).json()
                    if req['state'] == "Success":
                        append_out_text("New {chest_type} crate available! {start_result} opening, ID: {chestid}".format(chest_type=chest['type'],start_result=req['state'],chestid=req['data']['id']))
                elif chest['ended_at'] < 0:
                    get_mg_token()
                    data_to_open = {
                        'chest_id':chest['id'],
                        'paid':0
                        }
                    url = "https://wf.my.com/minigames/craft/api/open"
                    req = s.post(url,data=data_to_open)
                    to_open_json = json.loads(req.text)
                    append_out_text("{chest_type} crate opening...\n    Content -> Level: {level} | Amount: {amount}".format(chest_type=chest['type'],level=to_open_json['data']['resource']['level'],amount=to_open_json['data']['resource']['amount']))
        app.after(30000,check_crates)
        
    print("Opening Main app")
    login_window.destroy()
    user_check_json = s.get('https://wf.my.com/minigames/bp/user-info').json()
    app = Tk() 
    app.title("Warface Crate Manager - {}".format(user_check_json['data']['username']))
    app.resizable(False, False)
    app.geometry("700x400")
    menubar = Menu(app)
    menubar.add_command(label="Resources", command=resources)
    menubar.add_command(label="Crates", command=crates)
    menubar.add_command(label="About", command=about_window)
    menubar.add_command(label="Update", command=check_for_updates)
    # display the menu
    app.config(menu=menubar)
    
    out_text = Text(app,  width=85)
    out_text.pack()
    user_check_json = s.get('https://wf.my.com/minigames/bp/user-info').json()
    out_text.insert(END,"Logged in as {}".format(user_check_json['data']['username']))
    app.after(30000,check_crates)
    app.mainloop()
    
def about_window():
    print("Opening About window")
    about_app = Tk()
    about_app.title("About")
    about_app.resizable(False, False)
    about_app.geometry("400x200")
    Label(about_app, text="\nDesigned by").pack()
    Label(about_app, text="seanwlk",fg="Light sky blue", font=("Helvetica", 16)).pack()
    Label(about_app, text="Version: {}".format(__version__)).pack()
    Label(about_app, text="Email: seanwlk@my.com").pack()
    Label(about_app, text="\nPowered by Python 3",font=("Calibri", 10)).pack()

def get_mg_token():
    get_token = s.get('https://wf.my.com/minigames/user/info').json()
    s.cookies['mg_token'] = get_token['data']['token']

def steam_login():
    # Steam login process by sumfun4WF
    user = wa.WebAuth(email.get(), password.get())
    try:
        user.login()
    except wa.CaptchaRequired:
        captcha_code = simpledialog.askstring("Captcha Code", "{}".format(user.captcha_url),parent=login_window)
        user.login(captcha=captcha_code)
    except wa.EmailCodeRequired:
        email_code = simpledialog.askstring("Email Code", "CODE",parent=login_window)
        user.login(email_code=email_code)
    except wa.TwoFactorCodeRequired:
        tfa_code = simpledialog.askstring("2 Factor", "CODE",parent=login_window)
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
    main_app()
    
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
        'email':email.get(),
        'password':password.get(),
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
    main_app()

### LOGIN WINDOW
def login(event=None):
    CREDS = {}
    CREDS['is_Steam'] = is_Steam.get()
    CREDS['email'] = email.get()
    CREDS['password'] = password.get()
    with open('creds.json','w') as json_file:
        json.dump(CREDS, json_file, indent=4, sort_keys=True)
    if is_Steam.get() == 0:
        print ("Login as My.com")
        mycom_login()
    elif is_Steam.get() == 1:
        print ("Login as Steam")
        steam_login()

login_window = Tk()   
login_window.resizable(False, False)
login_window.geometry("350x100")
login_window.title("Login")

email = StringVar() #Email variable
password = StringVar() #Password variable
is_Steam = IntVar()

if os.path.isfile('./creds.json'):
    with open('creds.json','r') as json_file:
        CREDS = json.load(json_file)
    is_Steam.set(CREDS['is_Steam'])
    email.set(CREDS['email'])
    password.set(CREDS['password'])

# Steam true/false
Checkbutton(login_window, text="Is Steam?", variable=is_Steam).grid(row=0,column=0,sticky = W)

# Email field 
Label(login_window, text="Email").grid(row=1,column=0,sticky = W)
emailEntry = Entry(login_window, textvariable=email, width=40)
emailEntry.grid(row=1,column=1,sticky = W)
emailEntry.focus()

# Password field 
Label(login_window, text="Password").grid(row=2,column=0,sticky = W)
passEntry = Entry(login_window, textvariable=password, show='*')
passEntry.grid(row=2,column=1,sticky = W)

# Login button
submit = Button(login_window, bd =2,text='Login',command=login).grid(row=3,column=1)  
login_window.bind('<Return>',login)

login_window.mainloop() 

### END LOGIN WINDOW     
  