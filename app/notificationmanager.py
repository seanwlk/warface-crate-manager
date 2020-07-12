import os
from plyer import notification
from plyer import platforms

class notificationManager:
  def __init__(self,app):
    self.app = app
    if os.path.isfile('C:\MyGames\Warface My.Com\GameIcon.ico'):
      self.appIcon = 'C:\MyGames\Warface My.Com\GameIcon.ico'
    elif os.path.isfile('C:\MyGames\Warface\GameIcon.ico'):
      self.appIcon = 'C:\MyGames\Warface My.Com\GameIcon.ico'
    elif os.path.isfile('C:\GamesMailRu\Warface\GameIcon.ico'):
      self.appIcon = 'C:\GamesMailRu\Warface\GameIcon.ico'
    else:
      self.appIcon = None
  def send(self, title, body):
    if self.app.configs.get("configs")['notifications']:
      notification.notify(title=title, message=body, app_name='Warface Crate Manager', app_icon=self.appIcon, timeout=5, ticker='', toast=False)
    return