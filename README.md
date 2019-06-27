# Warface Automatic Crate Manager
Python script that automatically opens new crates for you and avoids you missclicking on wrong buttons that make you spend BattlePoints for no reason (which is the main reason this script was designed for).
New version with GUI and simple usage for users that don't know how to setup python enviroment.

**You will never need to open battlepass website agian with this tool!**

# Requisites for running the non-compiled version
- Python3
- Tkinter
- Python `requests` module
- Python `steam` module
- Python `lxml` module
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
#### Armageddon profile
![Profile](https://i.imgur.com/umQHMsP.png)
#### Armageddon week viewer
![Weeks](https://i.imgur.com/uq7G5Uf.png)

# Credits
- Original project and design - [@seanwlk](https://github.com/seanwlk)
- Steam support - [@sumfun4WF](https://github.com/sumfun4WF)