import tkinter as tk
from tkinter import messagebox

class _bpProfileWindow:
  def __init__(self, app):
    self.app = app
  def show(self):
    self.window = tk.Tk()
    self.window.title("Battlepass profile")
    self.window.resizable(False, False)
    self.window.geometry("400x360")
    uprofile = self.app.accountManager.get("https://$baseurl$/minigames/battlepass/user/info")
    wallets = self.app.accountManager.get("https://$baseurl$/minigames/battlepass/wallets")
    tk.Label(self.window, text=f"{self.app._currentBattlepass} Access: {self.memberCheck(uprofile['data'])}").grid(row=0, sticky=tk.W)
    tk.Label(self.window, text="Tokens: {}".format(wallets['data']['soft'])).grid(row=1, sticky=tk.W)
    tk.Label(self.window, text="Rare Tokens: {}".format(wallets['data']['hard'])).grid(row=2, sticky=tk.W)
    tk.Label(self.window, text="Victories: {}/5".format(wallets['data']['victory'])).grid(row=3, sticky=tk.W)
    freecrateFrame = tk.Frame(self.window)
    freecrateFrame.grid(row=4, sticky=tk.W)
    if wallets['data']['victory'] >= 5:
      tk.Label(freecrateFrame, text="5 wins reached. You can claim your free crate.").grid(row=0, sticky=tk.W)
      tk.Button(freecrateFrame, bd=2, text='Open',command=self.openFreeCrate).grid(row=1, sticky=tk.W)
  def openFreeCrate(self):
    req = self.app.accountManager.post("https://$baseurl$/minigames/battlepass/box/open",data={"id":5,"count":1,"currency":3})
    print (req) # DEBUG
    if len(req['data']) == 0:
      content = "There were no rewards in this crate" # Is this possible?
    else:
      item = req['data'][0]
      if 'permanent' in item['reward']['item'].values() or 'permanent' in item['reward']['item']:
        content = item['title']+ " - Permanent"
      elif 'consumable' in item['reward']['item'].values() or 'consumable' in item['reward']['item']:
        content = item['title']+ " - Amount: {}".format(item['count'])
      elif 'regular' in item['reward']['item'].values() or 'regular' in item['reward']['item']:
        content = item['title']
      else:
        content = item['title']+ " - {0} {1}".format(item['reward']['item']['duration'],item['reward']['item']['duration_type'])
    messagebox.showinfo("Free crate opened", "Content: \n{}".format(content))
  def memberCheck(self,data):
    if data['status'] == "member":
      return "YES"
    return "NO"
