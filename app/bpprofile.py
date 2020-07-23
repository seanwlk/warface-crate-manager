import tkinter as tk
from tkinter import messagebox

class _bpProfileWindow:
  def __init__(self, app):
    self.app = app
  def show(self):
    self.window = tk.Tk()
    self.window.title("Battlepass profile")
    self.window.resizable(False, False)
    self.window.geometry("400x450")
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
      tk.Button(freecrateFrame, bd=2, text='Open Free',command=lambda:self.openFreeCrate("free")).grid(row=1, sticky=tk.W)
    if wallets['data']['victory_vip'] >= 5:
      tk.Label(freecrateFrame, text="5 wins reached. You can claim your free VIP crate.").grid(row=2, sticky=tk.W)
      tk.Button(freecrateFrame, bd=2, text='Open VIP',command=lambda:self.openFreeCrate("vip")).grid(row=3, sticky=tk.W)
    bpstats = self.app.accountManager.get("https://$baseurl$/minigames/battlepass/stat")['data']
    tk.Label(self.window, text="Player stats", font=('Arial',11,'bold')).grid(row=5, sticky=tk.NW)
    tk.Label(self.window, text="PVP", font=('Arial',9,'bold','underline')).grid(row=6, sticky=tk.W)
    tk.Label(self.window, text="Rating: {}".format(bpstats['pvp']['rating'])).grid(row=7, sticky=tk.W)
    tk.Label(self.window, text="KD: {}".format(bpstats['pvp']['stats']['kd'])).grid(row=8, sticky=tk.W)
    tk.Label(self.window, text="Headshots: {}".format(bpstats['pvp']['stats']['headshots'])).grid(row=9, sticky=tk.W)
    tk.Label(self.window, text="Ranked: {}".format(bpstats['pvp']['stats']['compet_rank'])).grid(row=10, sticky=tk.W)
    tk.Label(self.window, text="Average slides: {}".format(bpstats['pvp']['stats']['slide'])).grid(row=11, sticky=tk.W)
    tk.Label(self.window, text="Explosives: {}".format(bpstats['pvp']['stats']['explosive'])).grid(row=12, sticky=tk.W)
    tk.Label(self.window, text="Global event", font=('Arial',9,'bold','underline')).grid(row=13, sticky=tk.W)
    tk.Label(self.window, text="Rating: {}".format(bpstats['event']['rating'])).grid(row=14, sticky=tk.W)
    tk.Label(self.window, text="Daily challenges: {}".format(bpstats['event']['stats']['daily'])).grid(row=15, sticky=tk.W)
    tk.Label(self.window, text="Common: {}".format(bpstats['event']['stats']['common'])).grid(row=16, sticky=tk.W)
    tk.Label(self.window, text="Claimed rewards: {}".format(bpstats['event']['stats']['rewards'])).grid(row=17, sticky=tk.W)
  def openFreeCrate(self,crateType):
    if crateType == "vip":
      crateID = 6
      currencyID = 4
    elif crateType == "free":
      crateID = 5
      currencyID = 3
    req = self.app.accountManager.post("https://$baseurl$/minigames/battlepass/box/open",data={"id":crateID,"count":1,"currency":currencyID})
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
