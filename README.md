# ninjaInfo.py - A simple tool

## What is NinjaInfo ?
NinjaInfo is basically an OSINT tool made to do geolocation with phone number or IP address and scrap e-mail IDs from the target URL as well, if given.
It also has a feature to tell the known framework used by the website just by looking over its `favicon.ico` file.

## How to install and run?
You can clone the github repository and then install the necessary python3 modules required to run NinjaInfo. If you don't have python3 installed then you can install it just by simple command : `sudo apt install python3` in debian based distros. After setting up your python3 enviroment clone the repository by running the commnad : `git clone https://github.com/whoami546/NinjaInfo.git`.

After cloning the repo go to the NinjaInfo's direcotry and there you will have a ``requirements-dev.txt`` file. In `requirements-dev.txt` there are the names of the modules that you need to install for using NinjaInfo. You can install those modules by simply running `sudo pip3 install -r requirements-dev.txt`. Before using this tool we have gone through following commands to do setup:-
* `git clone https://github.com/whoami546/NinjaInfo.git`
* `cd NinjaInfo/`
* `sudo pip3 install -r requirements-dev.txt`
* `chmod 740 ninjaInfo.py`

That's all it takes to install.... Now feel free to use this tool. And If you want to use this tool without navigating to `ninjaInfo.py`'s path then do `sudo mv /usr/local/bin/`.
