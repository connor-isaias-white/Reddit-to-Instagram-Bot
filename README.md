# Reddit to Instagram bot
This is a bot that takes the top posts of a subreddit and posts them to
## Installation
Clone or download then install requirements

open a terminal and type:
~~~~
git clone https://github.com/connor-isaias-white/Reddit-to-Instagram-Bot.git
cd Reddit-to-Instagram-Bot
pip install -r requirements.txt
~~~~
or `pip3 install -r requirements.txt` if you use pip3
## Setup
Open config.py and fill out all the fields

If you don't have a Reddit account you can make one [here](https://www.reddit.com/register "Sign up")
and an Instagram account [here](https://www.instagram.com/accounts/emailsignup/?hl=en "Sign up")

Then to create a client_id and client_secret go to https://www.reddit.com/prefs/apps and click create app, give it a name, select script and fill in remaining text boxes

![example](/files/readmefiles/makeapp.png)
This should give you a secret and a client id:

![example](/files/readmefiles/ids.png)
Use these to fill out config.py
## Run
To run the bot run `python main.py` or `python3 main.py` in the directory Reddit-to-Instagram-Bot and leave running.

If you have any questions feel free to ask

## To Do
add support for gifs
