# BOTA  
BOT-A is a free Discord Dota 2 bot which provides comprehensive Information of every Dota 2 characters and exciting features for the community. Pull request are welcome and report any issues you find.  
  
[![Join FredBoat Hangout](https://i.imgur.com/oWXj1vI.png)](https://discord.gg/a7QYPWd)  [![Join FredBoat Hangout](https://i.imgur.com/eBAIETS.jpg)](https://discordapp.com/api/oauth2/authorize?client_id=501100945405378562&permissions=388176&scope=bot)

## Commands & Screenshots
Commands can be found at at [here](http://bota.ml/index.html#table1-7)
Screenshots:
1. Command:  !counter  morphling  ![counter morphling](http://bota.ml/assets/images/counter-morph-full-818x415.png)
2. Command:  !item storm ![item storm](http://bota.ml/assets/images/items-storm-1077x619.png)
3. Command:  !profile midone ![profile](http:bota.ml/assets/images/profile-midone-1355x802.png)

## Setup
### Pre-Requirements:
Before setting up the environment we first need to get:
1. Discord Token
2. Discord Client ID
3. Dota2 API key
4. Discord User (Optional)

* To get `Discord Token` and `Discord Client ID` you can check [this](http://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
* You can get your  `Dota2 API key` from [here](https://steamcommunity.com/dev/apikey)
* You can get your `Discord User` by clicking on your profile in discord. It will look like `YourName#1234` eg: `bendang#3278`

Once this is done you can assign all this key values in `private_constant.py`.

### Install Requirements
```bash
sudo sh setup.sh
```
### Run
**Run the bot**
```bash
sh run_bota.sh
```
`run_bota.sh` runs two programs parallely on the screen background:
1. `main.py`: This is the bot application server where all commands are executed
2. `background_scrap.py`: This program is activated twice a day to update our data.

**Stop the bot**
```bash
sh stop_bota.sh
```

### Data Collection Source
1. [DotaBuff](https://www.dotabuff.com/)
2. [Reddit](https://www.reddit.com/r/DotA2/)
3. [Twitch](https://www.twitch.tv/)
4. Dota2API