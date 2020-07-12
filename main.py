import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from wfaccountmanager import WFAccountManager
from app.configmanager import configManager
from app.routinemanager import routineManager
from app.notificationmanager import notificationManager
from app.update import updateManager
from app.loginwindow import LoginWindow
from app.configwindow import _ConfigWindow
from app.bpprofile import _bpProfileWindow
from app.bptasks import _bpTasksWindow
from app.resources import _resourcesWindow
from app.crates import _cratesWindow
from app.about import _aboutWindow


class WFCrateManager:
  def __init__(self, master):
    self.master = master
    self.configs = configManager(os.path.dirname(os.path.realpath(__file__)))
    self.appVersion = "2.0"
    self._currentBattlepass = "Gorgona"
    LoginWindow(master,self)
    # App Windows
    self.configWindow = _ConfigWindow(self)
    self.bpProfile = _bpProfileWindow(self)
    self.bpTasks = _bpTasksWindow(self)
    self.resources = _resourcesWindow(self)
    self.crates = _cratesWindow(self)
    self.about = _aboutWindow(self)
    self.update = updateManager(self)
    self.notif = notificationManager(self)
  def renderApp(self):
    self.app = tk.Tk()
    self.app.title(f"Warface Crate Manager - {self.user['username']}")
    self.app.resizable(False, False)
    self.app.geometry("700x400")
    self.menubar = tk.Menu(self.app)
    bp = tk.Menu(self.menubar, tearoff=0)
    self.menubar.add_cascade(label=self._currentBattlepass, menu=bp)
    bp.add_command(label="Profile", command=lambda:self.bpProfile.show())
    bp.add_command(label="Daily Tasks", command=lambda:self.bpTasks.show())
    self.menubar.add_command(label="Resources", command=lambda:self.resources.show())
    self.menubar.add_command(label="Crates", command=lambda:self.crates.show())
    self.menubar.add_command(label="About", command=lambda:self.about.show())
    self.menubar.add_command(label="Update", command=lambda:self.update.check())
    self.menubar.add_command(label="Config", command=lambda:self.configWindow.show())
    self.app.config(menu=self.menubar)
    self.out_text = tk.Text(self.app, width=85)
    self.out_text.pack()
    self.consoleLog(f"Logged in as {self.user['username']}")
    self.update.check(silent=True)
    # Routines
    self.routines = routineManager(self,self.app)
    self.routines.checkCrates()
    self.routines.checkFreeCrate()
    self.routines.checkTasks()
    self.app.mainloop()
  def consoleLog(self,log):
    self.out_text.configure(state='normal')
    self.out_text.insert(tk.END,f"\n[{time.strftime('%b %d %T')}] {log}")
    self.out_text.see("end")
    self.out_text.configure(state='disabled')
  def login(self,region,lang,account,password):
    self.accountManager = WFAccountManager(region,lang=lang)
    if region == "steam":
      return self._steamloginHandler(account,password,lang)
    else:  
      self.accountManager.login(account,password)
      self.user = self.accountManager.me
      self.master.destroy()
      self.configs.set("region",region)
      self.configs.set(region,{"email":account,"password":password})
      self.configs.set("lang",lang)
      self.renderApp()
  def _steamloginHandler(self,account,password,lang):
    steamConfs = self.configs.get("steam")
    if steamConfs:
      if "steamID" in steamConfs and "auth_token" in steamConfs and "steamguard_token" in steamConfs:
        self.accountManager.login(steamID=steamConfs['steamID'],auth_token=steamConfs['auth_token'],steamguard_token=steamConfs['steamguard_token'])
        self.user = self.accountManager.me
        self.master.destroy()
        self.renderApp()
        if self.user['state'] != "auth":
          messagebox.showinfo(title="Steam Oauth2 expired or invalid", message="You steam Oauth2 keys are invalid or expired. They will be deleted, proceed restarting the app to refresh them.")
          self.configs.set("steam",{"email":account,"password":password})
        return None
    d = self.accountManager.login(account,password)
    if d['status'] == 0:
      pass
    elif d['status'] == 1:
      captcha_code = simpledialog.askstring("Captcha Code", "{}".format(d['url']),parent=self.master)
      oauth2 = self.accountManager.postSteam2FA(captcha_code)
    elif d['status'] == 2:
      email_code = simpledialog.askstring("Email Code", "CODE",parent=self.master)
      oauth2 = self.accountManager.postSteam2FA(email_code)
    elif d['status'] == 3:
      tfa_code = simpledialog.askstring("2 Factor", "CODE",parent=self.master)
      oauth2 = self.accountManager.postSteam2FA(tfa_code)
    self.user = self.accountManager.me
    self.master.destroy()
    self.renderApp()
    self.configs.set("region","steam")
    if oauth2:
      self.configs.set("steam",{"email":account,"password":password,"steamID":oauth2['steam']['steamID'],"auth_token":oauth2['steam']['auth_token'],"steamguard_token":oauth2['steam']['steamguard_token']})
    else:
      self.configs.set("steam",{"email":account,"password":password})
    self.configs.set("lang",lang)

def main():
  root = tk.Tk()
  crateManager = WFCrateManager(root)
  root.mainloop()

if __name__ == '__main__':
  main()