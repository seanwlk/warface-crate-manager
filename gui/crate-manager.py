 #!/usr/bin/env python3
 # -*- coding: utf-8 -*-

__author__ = "seanwlk"
__copyright__ = "Copyright 2019"
__license__ = "GPL"
__version__ = "1.96"

import sys, os
import datetime,time
import requests
import json
import steam.webauth as wa
import steam.steamid as sid
import steam.util.web as sweb
from collections import OrderedDict
from io import StringIO
import lxml.html
from tkinter import *
from tkinter import ttk,simpledialog,messagebox
from functools import partial
dir_path = os.path.dirname(os.path.realpath(__file__))
s = requests.Session()
__currentOperation = "Gorgona"

def check_for_updates(silent=False):
  def update():
    def downloadUpdate(name,url):
      req = requests.get(url)
      open (name,'wb').write(req.content)
      messagebox.showinfo("Download completed","The download of {} was completed. It is now in the same path as this executable. \nYou can now proceed un-zipping the file and replacing the old ones. Make sure to save creds.json".format(name))
    update_window = Tk()
    update_window.title("Update")
    update_window.resizable(False, False)
    update_window.geometry("350x280")
    Label(update_window, text="Available versions",fg="Light sky blue", font=("Helvetica", 16)).pack()
    Label(update_window,text="GUI: contains just the exe file and all the libraries packed inside\nUnpacked: libraries are separate from executable, making \n it faster and lighter on low end PCs").pack()
    Label(update_window).pack()
    for index,asset in enumerate(ver['assets']):
      assetFrame = Frame(update_window)
      assetFrame.pack()
      Label(assetFrame,text=asset['name']).pack()
      Button(assetFrame,bd=2,text="Download",command=partial(downloadUpdate,asset['name'],asset['browser_download_url'])).pack()
    update_window.mainloop()
  ver = requests.get("https://api.github.com/repos/seanwlk/warface-crate-manager/releases/latest").json()
  print("Looking for udpates")
  if __version__ < ver['tag_name']:
    user_response = messagebox.askquestion("New version available!","You are currently running version {current} but {latest} is available.\n\nChangelog:\n{changes}".format(current=__version__,latest=ver['tag_name'],changes=ver['body']),icon='warning')
    if user_response == "yes":
      update()
  else:
    if not silent:
      messagebox.showinfo("No updates available","You are currently running the latest version of the project.")

def resources():
  print("Opening available resources window")
  resources_window = Tk()
  resources_window.title("Resources")
  resources_window.resizable(False, False)
  resources_window.geometry("225x130")
  main_json = s.get("https://{}/minigames/craft/api/user-info".format(base_url)).json()
  level1=main_json['data']['user_resources'][0]['amount']
  level2=main_json['data']['user_resources'][1]['amount']
  level3=main_json['data']['user_resources'][2]['amount']
  level4=main_json['data']['user_resources'][3]['amount']
  level5=main_json['data']['user_resources'][4]['amount']

  current_res_labels = ttk.Labelframe(resources_window, text='Current Resources')
  current_res_labels.grid(row=0,column=0,sticky = W)
  Label(current_res_labels, text="Level 1: {}".format(level1)).grid(row=0,column=0,sticky = W)
  Label(current_res_labels, text="Level 2: {}".format(level2)).grid(row=1,column=0,sticky = W)
  Label(current_res_labels, text="Level 3: {}".format(level3)).grid(row=2,column=0,sticky = W)
  Label(current_res_labels, text="Level 4: {}".format(level4)).grid(row=3,column=0,sticky = W)
  Label(current_res_labels, text="Level 5: {}".format(level5)).grid(row=4,column=0,sticky = W)

  Label(resources_window).grid(row=0,column=1,sticky = W) #Space

  converted_res = ttk.Labelframe(resources_window, text='If all converted')
  converted_res.grid(row=0,column=2,sticky = W)
  Label(converted_res, text="Level 1: {}".format(level1%50)).grid(row=0,column=0,sticky = W)
  level2 = level2 + int(level1/50)
  Label(converted_res, text="Level 2: {}".format(level2%50)).grid(row=1,column=0,sticky = W)
  level3 = level3 + int(level2/50)
  Label(converted_res, text="Level 3: {}".format(level3%35)).grid(row=2,column=0,sticky = W)
  level4 = level4 + int(level3/35)
  Label(converted_res, text="Level 4: {}".format(level4%25)).grid(row=3,column=0,sticky = W)
  level5 = level5 + int(level4/25)
  Label(converted_res, text="Level 5: {}".format(level5)).grid(row=4,column=0,sticky = W)

def crate_date(end_at):
  if end_at > 0:
    return "Opens in {}".format(str(datetime.timedelta(seconds=end_at)))
  else:
    return "Crate Open"

def crates():
  print("Opening available crates window")
  crates_window = Tk()
  crates_window.title("Crates")
  crates_window.resizable(False, False)
  crates_window.geometry("250x200")
  main_json = s.get("https://{}/minigames/craft/api/user-info".format(base_url)).json()
  Label(crates_window).grid(row=0,column=1,sticky = W)
  Label(crates_window, text="Type").grid(row=0,column=1,sticky = N)
  Label(crates_window, text="Status").grid(row=0,column=2,sticky = N)
  for index,crate in enumerate(main_json['data']['user_chests']):
    square_icon = Canvas(crates_window, width=15, height=15)
    square_icon.grid(row=index+1,column=0,sticky = W)
    if crate['type'] == "platinum":
      square_icon.create_rectangle(0, 0, 15, 15, fill="black")
    elif crate['type'] == "gold":
      square_icon.create_rectangle(0, 0, 15, 15, fill="yellow")
    elif crate['type'] == "silver":
      square_icon.create_rectangle(0, 0, 15, 15, fill="silver")
    elif crate['type'] == "common":
      square_icon.create_rectangle(0, 0, 15, 15, fill="white")
    Label(crates_window, text="{}".format(crate['type'].capitalize())).grid(row=index+1,column=1,sticky = W)
    Label(crates_window, text="{}".format("New" if crate['state'] == "new" else crate_date(crate['ended_at']))).grid(row=index+1,column=2,sticky = W)

class VerticalScrolledFrame:
  def __init__(self, master, **kwargs):
    width = kwargs.pop('width', None)
    height = kwargs.pop('height', None)
    bg = kwargs.pop('bg', kwargs.pop('background', None))
    self.outer = Frame(master, **kwargs)

    self.vsb = Scrollbar(self.outer, orient=VERTICAL)
    self.vsb.pack(fill=Y, side=RIGHT)
    self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
    self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
    self.canvas['yscrollcommand'] = self.vsb.set
    self.canvas.bind("<Enter>", self._bind_mouse)
    self.canvas.bind("<Leave>", self._unbind_mouse)
    self.vsb['command'] = self.canvas.yview

    self.inner = Frame(self.canvas, bg=bg)
    self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
    self.inner.bind("<Configure>", self._on_frame_configure)

    self.outer_attr = set(dir(Widget))

  def __getattr__(self, item):
    if item in self.outer_attr:
      return getattr(self.outer, item)
    else:
      return getattr(self.inner, item)

  def _on_frame_configure(self, event=None):
    x1, y1, x2, y2 = self.canvas.bbox("all")
    height = self.canvas.winfo_height()
    self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

  def _bind_mouse(self, event=None):
    self.canvas.bind_all("<4>", self._on_mousewheel)
    self.canvas.bind_all("<5>", self._on_mousewheel)
    self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

  def _unbind_mouse(self, event=None):
    self.canvas.unbind_all("<4>")
    self.canvas.unbind_all("<5>")
    self.canvas.unbind_all("<MouseWheel>")

  def _on_mousewheel(self, event):
    if event.num == 4 or event.delta > 0:
      self.canvas.yview_scroll(-1, "units" )
    elif event.num == 5 or event.delta < 0:
      self.canvas.yview_scroll(1, "units" )

def daily_tasks():
  def showRewards(rewards):
    data = []
    for r in rewards:
      if r['reward']['type'] == "game_item":
        if 'permanent' in r['reward']['item'].values() or 'permanent' in r['reward']['item']:
          data.append(r['title']+ " - Permanent")
        elif 'consumable' in r['reward']['item'].values() or 'consumable' in r['reward']['item']:
          data.append(r['title']+ " - Amount: {}".format(r['reward']['item']['count']))
        else:
          data.append(r['title']+ " - {0} {1}".format(r['reward']['item']['duration'],r['reward']['item']['duration_type']))
      elif r['reward']['type'] == "currency":
        if r['reward']['currency'] == "soft":
          data.append(str(r['reward']['count']) + ' Currency')
        elif r['reward']['currency'] == "hard":
          data.append(str(r['reward']['count']) + ' Rare Tokens')
      else:
        data.append(r['title']) # Will this even happen ?
    return "\n".join(data)
  print("Opening daily tasks window")
  todo_missions = Tk()
  todo_missions.title("{} missions to complete".format(__currentOperation))
  todo_missions.geometry("790x575")
  # main frame that contains multiple generated mission frames
  missionList = VerticalScrolledFrame(todo_missions)
  missionList.pack(fill="x", expand=True)
  tasks = s.get("https://{url}/minigames/battlepass/task/all".format(url=base_url)).json()
  tableFrame = Frame(missionList)
  tableFrame.pack(fill="x", expand=True)
  Label(tableFrame,text="Task").grid(row=0,column=0,sticky = W)
  Label(tableFrame,text="Rewards").grid(row=0,column=1,sticky = W)
  Label(tableFrame,text="Status").grid(row=0,column=2,sticky = W)
  hr=Frame(tableFrame,height=1,width=750,bg="black")
  hr.grid(row=0,columnspan=3,sticky = S)
  for index, task in enumerate(tasks['data']):
    index+=1
    taskFrame = Frame(tableFrame,borderwidth=0,relief=GROOVE,highlightthickness=0,highlightcolor="light grey")
    taskFrame.grid(row=index,column=0,sticky = W)
    Label(taskFrame,text="{}".format(task['title'])).grid(row=0,sticky = W)
    Label(taskFrame,text="Progress: {progress}/{target_count}".format(**task)).grid(row=1,sticky = W)
    hr=Frame(tableFrame,height=1,width=730,bg="black")
    hr.grid(row=index,columnspan=3,sticky = S)
    
    rewardFrame = Frame(tableFrame,borderwidth=0,relief=GROOVE,highlightthickness=0,highlightcolor="light grey")
    rewardFrame.grid(row=index,column=1,sticky = W)
    Label(rewardFrame,text="{}".format(showRewards(task['rewards'])),justify=LEFT).grid(row=0,rowspan=2,column=1,sticky = W)
    
    statusFrame = Frame(tableFrame,borderwidth=0,relief=GROOVE,highlightthickness=0,highlightcolor="light grey")
    statusFrame.grid(row=index,column=2,sticky = W)
    if task['is_complete']:
      Label(statusFrame,text="\u2713",fg="green",font=("Arial", 18)).grid(row=0,rowspan=2,column=0,sticky = E)
  missionList.pack(side=LEFT,fill=BOTH)

def go_profile():
  def openFreeCrate():
    req = s.post("https://{}/minigames/battlepass/box/open".format(base_url),data={"id":5,"count":1,"currency":3}).json()
    print (req) # DEBUG
    if len(req['data']) == 0:
      content = "There were no rewards in this crate" # Is this possible?
    else:
      item = req['data'][0]
      if 'permanent' in item['reward']['item'].values() or 'permanent' in item['reward']['item']:
        content = item['title']+ " - Permanent"
      elif 'consumable' in item['reward']['item'].values() or 'consumable' in item['reward']['item']:
        content = item['title']+ " - Amount: {}".format(item['count'])
      else:
        content = item['title']+ " - {0} {1}".format(item['reward']['item']['duration'],item['reward']['item']['duration_type'])
    messagebox.showinfo("Free crate opened", "Content: \n{}".format(content))

  print("Opening global operation profile")
  go_profile_wind = Tk()
  go_profile_wind.title("{} Profile".format(__currentOperation))
  go_profile_wind.geometry("400x360")
  uprofile = s.get("https://{}/minigames/battlepass/user/info".format(base_url)).json()
  wallets = s.get("https://{}/minigames/battlepass/wallets".format(base_url)).json()
  Label(go_profile_wind, text="Gorgona Access: {}".format("YES" if "gorgona" in uprofile['data']['accesses'] else "NO")).grid(row=0,sticky = W)
  Label(go_profile_wind, text="Tokens: {}".format(wallets['data']['soft'])).grid(row=1,sticky = W)
  Label(go_profile_wind, text="Rare Tokens: {}".format(wallets['data']['hard'])).grid(row=2,sticky = W)
  Label(go_profile_wind, text="Victories: {}/5".format(wallets['data']['victory'])).grid(row=3,sticky = W)
  freecrateFrame = Frame(go_profile_wind)
  freecrateFrame.grid(row=4,sticky = W)
  if wallets['data']['victory'] == 5:
    Label(freecrateFrame, text="5 wins reached. You can claim your free crate.").grid(row=0,sticky = W)
    Button(freecrateFrame, bd =2,text='Open',command=openFreeCrate).grid(row=1,sticky=W)

def main_app():
  check_for_updates(silent=True)
  def append_out_text(text):
    out_text.configure(state='normal')
    out_text.insert(END,"\n{}".format(text))
    out_text.configure(state='disabled')
  def check_crates():
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
            append_out_text("[{actiontime}] New {chest_type} crate available! {start_result} opening, ID: {chestid}".format(actiontime=time.strftime('%b %d %T'),chest_type=chest['type'],start_result=req['state'],chestid=req['data']['id']))
        elif chest['ended_at'] < 0:
          get_mg_token()
          data_to_open = {
            'chest_id':chest['id'],
            'paid':0
            }
          url = "https://{}/minigames/craft/api/open".format(base_url)
          req = s.post(url,data=data_to_open)
          to_open_json = json.loads(req.text)
          append_out_text("[{actiontime}] {chest_type} crate opening...\n    Content -> Level: {level} | Amount: {amount}".format(actiontime=time.strftime('%b %d %T'),chest_type=chest['type'],level=to_open_json['data']['resource']['level'],amount=to_open_json['data']['resource']['amount']))
    app.after(30000,check_crates)

  global task_history
  task_history = {}
  def check_tasks():
    temp = {}
    get_mg_token()
    req = s.get("https://{url}/minigames/battlepass/task/all".format(url=base_url)).json()
    for j, task in enumerate(req['data']):
      temp[j] = (task['is_complete'] == False)
      global task_history
      if task_history == {}:
        continue
      if temp[j] != task_history[j]:
        append_out_text("[{actiontime}] Task Completed : {description}".format(actiontime=str(time.strftime('%b %d %X')),description=task['title']))
    task_history = temp
    app.after(60000, check_tasks)

  print("Opening Main app")
  login_window.destroy()
  user_check_json = s.get('https://{}/minigames/user/info'.format(base_url)).json()
  app = Tk()
  app.title("Warface Crate Manager - {}".format(user_check_json['data']['username']))
  app.resizable(False, False)
  app.geometry("700x400")
  menubar = Menu(app)
  goOp = Menu(menubar, tearoff=0)
  menubar.add_cascade(label=__currentOperation, menu=goOp)
  goOp.add_command(label="Profile", command=go_profile)
  goOp.add_command(label="Daily Tasks", command=daily_tasks)
  menubar.add_command(label="Resources", command=resources)
  menubar.add_command(label="Crates", command=crates)
  menubar.add_command(label="About", command=about_window)
  menubar.add_command(label="Update", command=check_for_updates)
  # display the menu
  app.config(menu=menubar)

  out_text = Text(app,  width=85)
  out_text.pack()
  user_check_json = s.get('https://{}/minigames/user/info'.format(base_url)).json()
  out_text.insert(END,"Logged in as {}".format(user_check_json['data']['username']))
  app.after(30000,check_crates)
  task_history = {}
  app.after(20000, check_tasks)
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
  get_token = s.get('https://{}/minigames/user/info'.format(base_url)).json()
  s.cookies['mg_token'] = get_token['data']['token']

def steam_oAuthLogin(steamguard, token):
  steamguard = steamguard.split("||")
  steamid = sid.SteamID(steamguard[0])

  response = s.post('https://api.steampowered.com/IMobileAuthService/GetWGToken/v1/', data={'access_token': token}).json()['response']

  # No token in response
  if not 'token' in response or not 'token_secure' in response:
    return False

  # Build cookie list
  cookies = {
    'steamLogin': str("{id}||{token}".format(id=steamid, token=response['token'])),
    'steamLoginSecure': str("{id}||{token}".format(id=steamid, token=response['token_secure'])),
    'steamMachineAuth' + str(steamid): steamguard[1],
    'sessionid': sweb.generate_session_id()
  }

  # Create cookie jar
  jar = requests.cookies.RequestsCookieJar()
  for cookie in cookies:
    jar.set(cookie, cookies[cookie], domain='steamcommunity.com', path='/')

  return jar

def steam_login():
  # Steam login process by sumfun4WF & Harmdhast
  if 'steam' in CREDS:
    # Relog using saved tokens
    if 'auth_token' in CREDS["steam"] and 'steamguard_token' in CREDS["steam"]:
      authcookies = steam_oAuthLogin(CREDS['steam']['steamguard_token'], CREDS['steam']['auth_token'])
      s.cookies.update(authcookies)

  if not 'sessionid' in s.cookies.get_dict():
    user = wa.MobileWebAuth(email.get(), password.get()) #MobileAuth should keep session alive
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
    # Save auth token for later session restore
    with open('creds.json','w') as json_file:
      CREDS['steam']['auth_token'] = user.oauth_token
      CREDS['steam']['steamguard_token'] = "{id}||{token}".format(id=user.steam_id.as_64, token=user.session.cookies.get_dict()["steamMachineAuth{id}".format(id=user.steam_id.as_64)])
      json.dump(CREDS, json_file, indent=4, sort_keys=True)
    # Copy cookies to session
    s.cookies.update(user.session.cookies)

  while True:
    try:
      entrance=s.get('https://auth-ac.my.games/social/steam?display=popup&continue=https%3A%2F%2Faccount.my.games%2Fsocial_back%2F%3Fcontinue%3Dhttps%253A%252F%252Faccount.my.games%252Foauth2%252F%253Fredirect_uri%253Dhttps%25253A%25252F%25252Fpc.warface.com%25252Fdynamic%25252Fauth%25252F%25253Fo2%25253D1%2526client_id%253Dwf.my.com%2526response_type%253Dcode%2526signup_method%253Demail%252Cphone%2526signup_social%253Dmailru%25252Cfb%25252Cvk%25252Cg%25252Cok%25252Ctwitch%25252Ctw%25252Cps%25252Cxbox%25252Csteam%2526lang%253Den_US%26client_id%3Dwf.my.com%26popup%3D1&failure=https%3A%2F%2Faccount.my.games%2Fsocial_back%2F%3Fsoc_error%3D1%26continue%3Dhttps%253A%252F%252Faccount.my.games%252Foauth2%252Flogin%252F%253Fcontinue%253Dhttps%25253A%25252F%25252Faccount.my.games%25252Foauth2%25252Flogin%25252F%25253Fcontinue%25253Dhttps%2525253A%2525252F%2525252Faccount.my.games%2525252Foauth2%2525252F%2525253Fredirect_uri%2525253Dhttps%252525253A%252525252F%252525252Fpc.warface.com%252525252Fdynamic%252525252Fauth%252525252F%252525253Fo2%252525253D1%25252526client_id%2525253Dwf.my.com%25252526response_type%2525253Dcode%25252526signup_method%2525253Demail%2525252Cphone%25252526signup_social%2525253Dmailru%252525252Cfb%252525252Cvk%252525252Cg%252525252Cok%252525252Ctwitch%252525252Ctw%252525252Cps%252525252Cxbox%252525252Csteam%25252526lang%2525253Den_US%252526client_id%25253Dwf.my.com%252526lang%25253Den_US%252526signup_method%25253Demail%2525252Cphone%252526signup_social%25253Dmailru%2525252Cfb%2525252Cvk%2525252Cg%2525252Cok%2525252Ctwitch%2525252Ctw%2525252Cps%2525252Cxbox%2525252Csteam%2526amp%253Bclient_id%253Dwf.my.com%2526amp%253Blang%253Den_US%2526amp%253Bsignup_method%253Demail%25252Cphone%2526amp%253Bsignup_social%253Dmailru%25252Cfb%25252Cvk%25252Cg%25252Cok%25252Ctwitch%25252Ctw%25252Cps%25252Cxbox%25252Csteam')
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
      s.get('https://auth-ac.my.games/sdc?from=https%3A%2F%2Faccount.my.games%2Foauth2%2F%3Fredirect_uri%3Dhttps%253A%252F%252Fpc.warface.com%252Fdynamic%252Fauth%252F%253Fo2%253D1%26client_id%3Dwf.my.com%26response_type%3Dcode%26signup_method%3Demail%2Cphone%26signup_social%3Dmailru%252Cfb%252Cvk%252Cg%252Cok%252Ctwitch%252Ctw%252Cps%252Cxbox%252Csteam%26lang%3Den_US%26signup%3D1')
      get_token = s.get('https://pc.warface.com/minigames/user/info').json()
      s.cookies['mg_token'] = get_token['data']['token']
      s.cookies['cur_language'] = op_lang()
    except:
      continue
    break
  main_app()

def mygames_login():
  payload = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie':'amc_lang=en_US; ',
    'DNT': '1',
    'Host': 'auth-ac.my.games',
    'Origin': 'https://account.my.games',
    'Referer': 'https://account.my.games/oauth2/login/?continue=https%3A%2F%2Faccount.my.games%2Foauth2%2F%3Fredirect_uri%3Dhttps%253A%252F%252Fpc.warface.com%252Fdynamic%252Fauth%252F%253Fo2%253D1%26client_id%3Dwf.my.com%26response_type%3Dcode%26signup_method%3Demail%2Cphone%26signup_social%3Dmailru%252Cfb%252Cvk%252Cg%252Cok%252Ctwitch%252Ctw%252Cps%252Cxbox%252Csteam%26lang%3Den_US&client_id=wf.my.com&lang=en_US&signup_method=email%2Cphone&signup_social=mailru%2Cfb%2Cvk%2Cg%2Cok%2Ctwitch%2Ctw%2Cps%2Cxbox%2Csteam',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
  login_data = {
    'email':email.get(),
    'password':password.get(),
    'continue':'https://account.my.games/oauth2/?redirect_uri=https%3A%2F%2Fpc.warface.com%2Fdynamic%2Fauth%2F%3Fo2%3D1&client_id=wf.my.com&response_type=code&signup_method=email,phone&signup_social=mailru%2Cfb%2Cvk%2Cg%2Cok%2Ctwitch%2Ctw%2Cps%2Cxbox%2Csteam&lang=en_US',
    'failure':'https://account.my.games/oauth2/login/?continue=https%3A%2F%2Faccount.my.games%2Foauth2%2Flogin%2F%3Fcontinue%3Dhttps%253A%252F%252Faccount.my.games%252Foauth2%252F%253Fredirect_uri%253Dhttps%25253A%25252F%25252Fpc.warface.com%25252Fdynamic%25252Fauth%25252F%25253Fo2%25253D1%2526client_id%253Dwf.my.com%2526response_type%253Dcode%2526signup_method%253Demail%252Cphone%2526signup_social%253Dmailru%25252Cfb%25252Cvk%25252Cg%25252Cok%25252Ctwitch%25252Ctw%25252Cps%25252Cxbox%25252Csteam%2526lang%253Den_US%26client_id%3Dwf.my.com%26lang%3Den_US%26signup_method%3Demail%252Cphone%26signup_social%3Dmailru%252Cfb%252Cvk%252Cg%252Cok%252Ctwitch%252Ctw%252Cps%252Cxbox%252Csteam&amp;client_id=wf.my.com&amp;lang=en_US&amp;signup_method=email%2Cphone&amp;signup_social=mailru%2Cfb%2Cvk%2Cg%2Cok%2Ctwitch%2Ctw%2Cps%2Cxbox%2Csteam',
    'nosavelogin':'0'
    }
  while True:
    try:
      r = s.post('https://auth-ac.my.games/auth',headers=payload,data=login_data, allow_redirects=False)
      for i in range(0,5):
        """
        1- Auth redirect to oauth2
        2- Oauth2 redirect to sdc
        3- Generates link to get to sdc token
        4- SDC token redirects to oauth2
        5- Auth link for pc.warface.com is generated
        6- GET auth link for session
        """
        r = s.get(r.headers['location'], allow_redirects=False)
      get_token = s.get('https://pc.warface.com/minigames/user/info').json()
      s.cookies['mg_token'] = get_token['data']['token']
      s.cookies['cur_language'] = op_lang()
    except:
      continue
    break
  main_app()

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
  s.get('https://auth.mail.ru/cgi-bin/auth?Login={mail}&Password={pwd}&FakeAuthPage=https%3A%2F%2Fwf.mail.ru%2Fauth'.format(mail=email.get(),pwd=password.get()))
  main_app()

def op_lang(*args):
  langs={
    "English" : "en",
    "Français" : "fr",
    "Deutsch" : "de",
    "Polski" : "pl",
    "Russian" : "ru",
    "中文" : "cn"
  }
  return langs[go_language.get()]

### LOGIN WINDOW
def login(event=None):
  global base_url
  CREDS['LoginType'] = LoginType.get()
  # Create LoginType key if it doesn't exist
  if not LoginType.get() in CREDS:
    CREDS[LoginType.get()] = {}
  # Reset saved tokens if username changes
  if LoginType.get() == "steam" and 'email' in CREDS['steam']:
    if not CREDS['steam']['email'] == email.get():
      CREDS[LoginType.get()] = {}
  CREDS[LoginType.get()]['email'] = email.get()
  CREDS[LoginType.get()]['password'] = password.get()
  with open('creds.json','w') as json_file:
    json.dump(CREDS, json_file, indent=4, sort_keys=True)
  if LoginType.get() == "mygames":
    print ("Login as My.games")
    base_url = "pc.warface.com"
    mygames_login()
  elif LoginType.get() == "steam":
    print ("Login as Steam")
    base_url = "pc.warface.com"
    steam_login()
  elif LoginType.get() == "mailru":
    print ("Login as Mail.ru")
    base_url = "wf.mail.ru"
    mailru_login()

def loginSelected(*args):
  try:
    email.set(CREDS[LoginType.get()]['email'])
  except KeyError:
    email.set("")
  try:
    password.set(CREDS[LoginType.get()]['password'])
  except KeyError:
    password.set("")

login_window = Tk()
login_window.resizable(False, False)
login_window.geometry("350x120")
login_window.title("Login")

email = StringVar() #Email variable
password = StringVar() #Password variable
LoginType = StringVar() # select login service, at the time only steam, mygames and mailru

if os.path.isfile('{}/creds.json'.format(dir_path)):
  with open('{}/creds.json'.format(dir_path),'r') as json_file:
    CREDS = json.load(json_file)
  try:
    LoginType.set(CREDS['LoginType'])
  except KeyError:
    LoginType.set("mygames")
  try:
    email.set(CREDS[CREDS['LoginType']]['email'])
  except KeyError:
    email.set("")
  try:
    password.set(CREDS[CREDS['LoginType']]['password'])
  except KeyError:
    password.set("")
else:
  CREDS = {}
  LoginType.set("mygames")

login_selector = Frame(login_window)
login_selector.grid(row=0, columnspan=3,sticky = W)
# Mygames true/false
Radiobutton(login_selector, text="My.games", variable=LoginType, value="mygames", command=loginSelected).grid(row=0,column=0,sticky = W)
# Steam true/false
Radiobutton(login_selector, text="Steam", variable=LoginType, value="steam", command=loginSelected).grid(row=0,column=1,sticky = W)
# Mail.ru true/false
Radiobutton(login_selector, text="Mail.ru", variable=LoginType, value="mailru", command=loginSelected).grid(row=0,column=2,sticky = W)

# Email field
Label(login_window, text="Email").grid(row=1,column=0,sticky = W)
emailEntry = Entry(login_window, textvariable=email, width=40)
emailEntry.grid(row=1,column=1,sticky = W)
emailEntry.focus()

# Password field
Label(login_window, text="Password").grid(row=2,column=0,sticky = W)
passEntry = Entry(login_window, textvariable=password, show='*')
passEntry.grid(row=2,column=1,sticky = W)

Label(login_window, text="Language").grid(row=3,column=0,sticky = W)
go_language=ttk.Combobox(login_window, width=10, values=["English","Français","Deutsch","Russian","中文"],state='readonly')
go_language.current(0)
go_language.grid(row=3,column=1,sticky = W) # Global operation language

# Login button
submit = Button(login_window, bd =2,text='Login',command=login).grid(row=4,column=1)
login_window.bind('<Return>',login)

login_window.mainloop()

### END LOGIN WINDOW
