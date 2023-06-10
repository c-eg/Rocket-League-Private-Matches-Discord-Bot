# Rocket League Private Matches Discord Bot
A discord bot to organise teams for private matches based on the user's set mmr.

## Preview
![image](https://user-images.githubusercontent.com/68134729/183295677-5a356790-edb4-4af1-b691-2348468d71d0.png)

## Features
- [x] 6 person queue
- [x] Multiple games on same server
- [x] Players can set their MMR
- [x] Teams can be decided with:
  - [x] Two captains
  - [x] Balanced by MMR
  - [x] Random
- [x] Queue for x amount of minutes
- [x] Slash commands

## Setting up for local development
1. Fork this repository
2. Install [Python 3.11](https://www.python.org/downloads/)
3. Install the libraries from requirements.txt
   - ```pip3 install -r requirements.txt```
4. Create a [Discord bot](https://discord.com/developers/docs/intro) (click on 'Applications'), getting the token
5. Rename .env_template to .env, adding values for each of the settings
6. Run the bot from ```main.py```

## License
GNU General Public License v3.0
