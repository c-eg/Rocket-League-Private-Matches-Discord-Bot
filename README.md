# Rocket League Private Matches Discord Bot #
[![License](https://img.shields.io/github/license/c-eg/Rocket-League-Private-Matches-Discord-Bot)](LICENSE)

Currently being used on the [UEA Rocket League Discord](https://discord.gg/Gam9qwJRAe) server

## Features Implemented ##
- [x] 6 person queue
- [ ] 4 Person queue
- [x] Multiple games on same server
- [x] Players can set their MMR
- [x] Teams can be decided with:
  - [x] Two captains
  - [x] Balanced by MMR
  - [x] Random
- [ ] Slash commands

## Setting up for local development ##
1. Fork this repository
2. Make sure you have the latest version of [Python 3](https://www.python.org/downloads/) installed
3. Install the libraries from requirements.txt
   - ```pip3 install -r requirements.txt```
4. Create a [Discord bot](https://discord.com/developers/docs/intro) (click on 'Applications')
5. Create a .env file on the same level as main.py and put the Discord bot's token into it e.g. ```BOT_TOKEN=XXXXXXXXX```
6. Run the bot from ```main.py```

## License ##
GNU General Public License v3.0
