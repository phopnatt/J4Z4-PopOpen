## Auto relaucnh roblox project
# This project is a python relauncher for roblox using customtkinter for gui
# There're auto relaunch function that check account by checking requst form roblox executor with http req function and also launch manualy
# and about endpoint stuff we are using fast api https://fastapi.tiangolo.com/
# and this is our robloxapisite function that will be wriiten in ConfigJ4Z$.lua  https://docs.potassium.pro/api-reference/introduction
---
## Core Folder
# Core folder is a folder that hold a tools to requst a authenication token from roblox And also save function was there

# accountcontrolCLI 
is an endpoint that accept heart  beat from roblox injector with their http request function that tell account alive if it not alive that modlue will rejoin roblox again if in Data/account.json in individulal account contains "Logged": true

# accountcontrolmodule
accountcontrolmodule is a module that load the account which contains "Logged": true 
in Data/account.json to GUI/Accountcontrol.py 
# accountmanagement
accountmanagement is a module to join roblox even from save etc.

# Filehandler
Filehandler is a moduleto save cooki and account name including check if that cookie still valid
---
## GUI Folder
# GUI Folder mostly contains gui event

# Accountcontrol

Accountcontrol is a folder that are stroke ui for auto rejoining if auto relaunch was toggle Core/accountcontrolCLI will be enable imagine is this ui is for automatic launching rather than manual launch in app.py or in main gui

# Accounteditor 
Accounteditor is a gui for main gui to add account

# accountlist

accountlist is a scrolling frame for main gui that contains account 

# app

app is a main gui for join account individualy and manualy 
---
## Data
# account.json
account.json is a save for account name and cookies in plain text
---
## Main.py
# is a main module that spawn each module 
## config.json 
# it's for saving settings in program (function that i will add in the future)
## ConfigJ4Z$.lua
# is a script for roblox executor side
---
## test.py is a just testing module just ignore it

