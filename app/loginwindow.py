import tkinter as tk
from tkinter import ttk

class LoginWindow:
  def __init__(self, master, app):
    self.master = master
    self.app = app
    self.master.resizable(False, False)
    self.master.geometry("350x120")
    self.master.title("Login")
    self.account = tk.StringVar()
    self.password = tk.StringVar()
    self.region = tk.StringVar()
    if self.app.configs.get("region"):
      self.region.set(self.app.configs.get("region"))
    else:
      self.region.set("west")
    login_selector = tk.Frame(self.master)
    login_selector.grid(row=0, columnspan=3,sticky = tk.W)
    tk.Radiobutton(login_selector, text="West", variable=self.region, value="west", command=self.loginSelected).grid(row=0,column=0,sticky = tk.W)
    tk.Radiobutton(login_selector, text="Steam", variable=self.region, value="steam", command=self.loginSelected).grid(row=0,column=1,sticky = tk.W)
    tk.Radiobutton(login_selector, text="Russia", variable=self.region, value="russia", command=self.loginSelected).grid(row=0,column=2,sticky = tk.W)
    tk.Label(self.master, text="Email").grid(row=1,column=0,sticky = tk.W)
    self.emailEntry = tk.Entry(self.master, textvariable=self.account, width=40)
    self.emailEntry.grid(row=1,column=1,sticky = tk.W)
    self.emailEntry.focus()
    tk.Label(self.master, text="Password").grid(row=2,column=0,sticky = tk.W)
    self.passEntry = tk.Entry(self.master, textvariable=self.password, show='*')
    self.passEntry.grid(row=2,column=1,sticky = tk.W)
    tk.Label(self.master, text="Language").grid(row=3,column=0,sticky = tk.W)
    self.lang=ttk.Combobox(self.master, width=10, values=["English","Français","Deutsch","Russian","中文"],state='readonly')
    self.lang.current(0)
    self.lang.grid(row=3,column=1,sticky = tk.W)
    tk.Button(self.master, bd =2,text='Login',command=self.login).grid(row=4,column=1)
    self.master.bind('<Return>',self.login)
    self.loginSelected() # Load creds on first run
  def login(self,*args):
    self.app.login(self.region.get(),self.lang.get(),self.account.get(),self.password.get())
  def loginSelected(self,*args):
    try:
      self.account.set(self.app.configs.get(self.region.get())['email'])
    except:
      self.account.set("")
    try:
      self.password.set(self.app.configs.get(self.region.get())['password'])
    except:
      self.password.set("")