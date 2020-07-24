import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class _seasonalShopWindow:
  def __init__(self, app):
    self.app = app
  def show(self):
    self.window = tk.Tk()
    self.window.title("Seasonal Shop")
    self.window.resizable(False, False)
    self.window.geometry("280x300")
    # boxes https://pc.warface.com/minigames/battlepass/box/all
    self.selectedCrate = tk.IntVar(master=self.window)
    self.selectedCurrency = tk.IntVar(master=self.window)
    self.selectedCrate.set(1)
    self.selectedCurrency.set(2)

    walletFrame = ttk.Labelframe(self.window, text='Resources')
    walletFrame.grid(row=0,columnspan=6, sticky=tk.W)
    self.wallets = self.app.accountManager.get("https://$baseurl$/minigames/battlepass/wallets")
    self.availableCrates = self.app.accountManager.get("https://$baseurl$/minigames/battlepass/box/all")['data']
    tk.Label(walletFrame, text="Normal: {}".format(self.wallets['data']['soft'])).grid(row=1, sticky=tk.W)
    tk.Label(walletFrame, text="Premium: {}".format(self.wallets['data']['hard'])).grid(row=2, sticky=tk.W)

    boxesFrame = ttk.Labelframe(self.window, text='Crates')
    boxesFrame.grid(row=1,columnspan=6,sticky=tk.W)
    tk.Radiobutton(boxesFrame, text="Camo", variable=self.selectedCrate, value=1).grid(row=0, column=0, sticky=tk.W)
    tk.Radiobutton(boxesFrame, text="Skin", variable=self.selectedCrate, value=2).grid(row=0, column=1, sticky= tk.W)
    tk.Radiobutton(boxesFrame, text="Achievements", variable=self.selectedCrate, value=3).grid(row=1, column=0, sticky=tk.W)
    tk.Radiobutton(boxesFrame, text="Gilboa Snake DBR", variable=self.selectedCrate, value=4).grid(row=1, column=1, sticky=tk.W)
    tk.Radiobutton(boxesFrame, text="Random Weapon", variable=self.selectedCrate, value=7).grid(row=2, column=0, sticky=tk.W)

    currencyFrame = ttk.Labelframe(self.window, text='Currency')
    currencyFrame.grid(row=2, columnspan=6, sticky=tk.W)
    tk.Radiobutton(currencyFrame, text="Normal", variable=self.selectedCurrency, value=2).grid(row=0, column=0, sticky=tk.W)
    tk.Radiobutton(currencyFrame, text="Premium", variable=self.selectedCurrency, value=1).grid(row=0, column=1, sticky=tk.W)

    openFrame = ttk.Labelframe(self.window, text='Amount')
    openFrame.grid(row=3, columnspan=6, sticky=tk.W)
    self.amount = tk.Spinbox(openFrame, width=3, from_=1, to=10)
    self.amount.grid(row=0, column=0, sticky=tk.W)
    tk.Button(openFrame, bd=2, text='Open', command=self.checkFunds).grid(row=0, column=1, sticky=tk.E)
  def checkFunds(self,*args):
    data = {
      "id": self.selectedCrate.get(),
      "count": self.amount.get(),
      "currency": "hard" if self.selectedCurrency.get() == 1 else "soft"
    }
    for c in self.availableCrates:
      if c['id'] == data['id']:
        for cur in c['conditions']['currencies']:
          if cur['currency'] == data['currency']:
            cost = cur['amount']
    totalcost = cost * int(data['count'])
    if totalcost > self.wallets['data'][data['currency']]:
      return messagebox.showerror("Not enough resources", f"You dont have enough fund to open the selected amount of crates.\nTotal cost: {totalcost}\nOwned: {self.wallets['data'][data['currency']]}", parent=self.window)
    return self._openBox()
  def _openBox(self,*args):
    #Currency 2: Normal, 1: Premium
    data = {
      "id": self.selectedCrate.get(),
      "count": self.amount.get(),
      "currency": self.selectedCurrency.get()
    }
    r = self.app.accountManager.post("https://$baseurl$/minigames/battlepass/box/open", data=data)
    for e in r['data']:
      if 'permanent' in e['reward']['item'].values() or 'permanent' in e['reward']['item']:
        content = e['title']+ " - Permanent"
      elif 'achievement' in e['reward']['item'].values() or 'achievement' in e['reward']['item']:
        content = "Achievement: "+ e['title']
      elif 'consumable' in e['reward']['item'].values() or 'consumable' in e['reward']['item']:
        content = e['title']+ " - Amount: {}".format(e['count'])
      elif 'regular' in e['reward']['item'].values() or 'regular' in e['reward']['item']:
        content = e['title']
      else:
        content = e['title']+ " - {0} {1}".format(e['reward']['item']['duration'],e['reward']['item']['duration_type'])
      self.app.consoleLog(f"Opened box -> {content}")
