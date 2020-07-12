import tkinter as tk

class _aboutWindow:
  def __init__(self, app):
    self.app = app
  def show(self):
    self.window = tk.Tk()
    self.window.title("About")
    self.window.resizable(False, False)
    self.window.geometry("400x200")
    tk.Label(self.window, text="\nDesigned by").pack()
    tk.Label(self.window, text="seanwlk", fg="Light sky blue", font=("Helvetica", 16)).pack()
    tk.Label(self.window, text=f"Version: {self.app.appVersion}").pack()
    tk.Label(self.window, text="Email: seanwlk@my.com").pack()
    tk.Label(self.window, text="\nPowered by Python 3", font=("Calibri", 10)).pack()