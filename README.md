# Warface Crate Manager
Python script that automatically opens new crates for you and avoids you missclicking on wrong buttons that make you spend BattlePoints for no reason (which is the main reason this script was designed for).
New version with GUI and simple usage for users that don't know how to setup python enviroment.

**You will never need to open battlepass website agian with this tool!**

# Requisites for running the non-compiled version
- Python3
- Tkinter
- Python `requests` module
- Python `wfaccountmanager` module
- Python `plyer` module
- 3 minutes to config
- Brain

# Requisites for compiled version
- A mouse with which you can double click the executable.
- A keyboard with which you can type login data
- Simply go to [Releases](https://github.com/seanwlk/warface-crate-manager/releases) and download latest compiled version

# Notice
For sake of usability, the credentials will be saved in the same folder as the script under the name `creds.json` (LOCALLY). This way when you login first time you will just have to run it next time and forget about it.

# Mail.ru login support
The login works but it may end up failing if you try to login multiple times requesting you to complete a captcha. I believe that it's IP block based from what i could see.
Just open your browser and go to wf.mail.ru, it will redirect you to the mail.ru verification captcha, just complete it once or twice and you will be able to login again.

# Images
#### Login
![Login](https://i.imgur.com/5TTsDfF.png)
#### Crate opening logs
![Main](https://i.imgur.com/gLjcwhC.png)
#### Current Crates
![Crates](https://i.imgur.com/g9DChMx.png)
#### Resource viewer
![Resources](https://i.imgur.com/aJY43Id.png)
#### Global operation menu
- Note that this may change from one battlepass to another. I always try to use the same templates but they always change something.
![Weeks](https://i.imgur.com/uq7G5Uf.png)
#### Notifications
- You can turn on notifications from configuration menu if you want. (It's turned off by default)
![notifs](https://i.imgur.com/nU1S5mI.jpg)
![notifs1](https://i.imgur.com/YbxKHEn.png)
![notifs2](https://i.imgur.com/imq80dW.png)

# Credits
- Original project and design - [@seanwlk](https://github.com/seanwlk)
- Original steam support and inspiration - [@sumfun4WF](https://github.com/sumfun4WF) / [@harmdhast](https://github.com/harmdhast)

## Donate
Please consider donating to support the project. It takes time to develop such apps during my free time.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/seanwlk)