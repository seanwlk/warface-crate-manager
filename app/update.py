import tkinter as tk
from tkinter import messagebox
import requests

class updateManager:
  def __init__(self, app):
    self.app = app
  def check(self,silent=False):
    ver = self.app.accountManager.get("https://api.github.com/repos/seanwlk/warface-crate-manager/releases/latest")
    if self.app.appVersion < ver['tag_name']:
      user_response = messagebox.askquestion("New version available!","You are currently running version {current} but {latest} is available.\n\nChangelog:\n{changes}".format(current=self.app.appVersion,latest=ver['tag_name'],changes=ver['body']),icon='warning')
      if user_response == "yes":
        self.updateWindow()
    else:
      if not silent:
        messagebox.showinfo("No updates available","You are currently running the latest version of the project.")
  def updateWindow(self):
    update_window = tk.Tk()
    update_window.title("Update")
    update_window.resizable(False, False)
    update_window.geometry("350x280")
    tk.Label(update_window, text="Available versions", fg="Light sky blue", font=("Helvetica", 16)).pack()
    tk.Label(update_window, text="GUI: contains just the exe file and all the libraries packed inside\nUnpacked: libraries are separate from executable, making \n it faster and lighter on low end PCs").pack()
    tk.Label(update_window).pack()
    ver = self.app.accountManager.get("https://api.github.com/repos/seanwlk/warface-crate-manager/releases/latest")
    for index,asset in enumerate(ver['assets']):
      assetFrame = tk.Frame(update_window)
      assetFrame.pack()
      tk.Label(assetFrame,text=asset['name']).pack()
      tk.Button(assetFrame,bd=2,text="Download",command=lambda:self._downloadUpdate(asset['name'],asset['browser_download_url'])).pack()
  def _downloadUpdate(self,name,url):
    req = requests.get(url)
    open (name,'wb').write(req.content)
    messagebox.showinfo("Download completed","The download of {} was completed. It is now in the same path as this executable. \nYou can now proceed un-zipping the file and replacing the old ones. Make sure to save creds.json".format(name))
    return