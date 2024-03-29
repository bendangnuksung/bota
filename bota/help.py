import discord
from bota import  constant
import random

BOTA_SUPPORT_SERVER_URL = "https://discord.gg/a7QYPWd"
BOTA_ADD_TO_SERVER_URL = "https://discordapp.com/api/oauth2/authorize?client_id=501100945405378562&permissions=388176&scope=bot"
PAYPAL_URL = 'https://www.paypal.me/bendang1'


HOW_TO_USE_COMMANDS_EXAMPLE = {
    '!profile': 'How to use:\n1. With SteamID:  `!profile 116585378`\n2. With Name: !profile midone`  (Save your name using `!save` command)`',
    '!save': 'How to use -> `!save midone 116585378`',
    '!counter': 'How to use -> `!counter axe`  `!counter zeus`',
    '!good': 'How to use -> `!good am`  `!good jugg`',
    '!skill': 'How to use -> `!skill phoenix`  `!good sf`',
    '!item': 'How to use -> `!item meepo`  `!item et`',
    '!twitch': 'How to use:\n `!twitch`   `!twitch en`   `!twitch ru`   `!twitch russian',
    '!reddit': 'How to use:\n 1. `!reddit`\n2. `!reddit hot`\n3. `!reddit new',
    '!pro': 'How to use:  `!pro slark`   `!pro meepo`',
    }

# Foot block
HELP_FOOTER = "NOTE: Can use short Hero Names, !counter anti mage ---as---> !counter am"
NOTE_FOOTER = " | Can use Short HeroName, !skill antimage -> !skill am"


NOTE_FOOTER_LIST = ['Can use Short HeroName, eg: !skill antimage -> !skill am',
                    'Get Twitch Live stream using: !twitch english, !twitch russian',
                    'Get current Top Games stats using: !topgame',
                    'You can also save and get your Profile stats. For details type !profile help',
                    'Get scepter/aghanim info of a hero. eg: !agha axe',
                    'Get a random reddit post from r/Dota2. !reddit',
                    'Alternative counter command: !counter axe -> !bad axe',
                    'Alternative skilll command: !skill axe -> !talent axe',
                    'Type !update to see any latest updates',
                    'Get weekly trends in Win Rate and Pick Rate: !trend',
                    'Want to counter meepo with a safelane hero? type: !counter meepo safe',
                    'Want to counter axe with midlane hero? type: !counter axe mid',
                    'Want to counter PA with offlane hero? type: !counter pa off',
                    'Check recent immortal/divine players item build using: !items HeroName',
                    'Check high win-rate Skill and Talent upgrade using: !skill HeroName',
                    'Know latest hero Meta with MMR brackets using: !meta',
                    'Watch Pro Player Perspective using: !pers HeroName',
                    'Get latest Pro Perspective videos using: !pers'
                    ]


def get_random_footer(prefix="!"):
    # global NOTE_FOOTER_LIST
    footer = random.choice(NOTE_FOOTER_LIST).replace("!", prefix)
    return footer


# Note
HERO_SHORT_NAME_NOTE = "**NOTE**: Can use short Hero Names, !counter anti mage  !counter am"


# Update Block
# UPDATE_BLOCK = 'Get Synergy hero for team with **`!synergy`**.\nType **`!synergy help`** for details'

# UPDATE_BLOCK = '**NEW**:' \
#                'To show only particular lane heroes that counter Anti Mage: **For EG:**\n' \
#                '1. Counter with support **`!counter am support`**\n' \
#                '2. Counter with midlane **`!counter am mid`**\n'\
#                'More Options: **`!counter help`** or **`!good help`**'

# UPDATE_BLOCK = 'Manage BOTA in your server using **`!guild`**\n' \
#                'Get Meta Hero with MMR brackets using **`!meta`**\n' \
#                '**`!items`** now shows starting items too'

# UPDATE_BLOCK = f'Watch Pro PLayer Perspective **@1440p60** on **YouTube** using: **`!pers HeroName`**\n' \
#                f'Please do __**[Subscribe Channel](https://www.youtube.com/channel/UCnby5VqRpcJ-qzyhAp2cTAQ)**__ to show support😊'

UPDATE_BLOCK = f'**Primal Beast** has been added in commands'

UPDATE_BLOCK_LIST=\
             ["`01-FEB-2021`: Watch Pro PLayer Perspective @1440p60 on **YouTube** **`!pers HeroName`**",
              "`04-JAN-2021`: Now !items shows starting items too",
              "`23-Dec-2020`: Added `!meta` command",
              "`23-Dec-2020`: Server owner can now change command prefix and block channels from BOTA, type `!guild` for details",
              "`15-Mar-2020`: User can now specify roles to show hero for !counter & !good command, type `!counter help`",
              "`30-Sep-2019`: Added Aghanim Info for heroes, type `!agha HeroName`",
              "`28-Sep-2019`: Added `!team` command, type `!team help` for details",
              "`25-Aug-2019`: Save your profile without name and change Steam ID and others, Type `!profile help` for details",
              "`15-Aug-2019`: Added TI command,   `!ti`",
              "`07-Aug-2019`: Added Language option in twitch    `!twitch en`  `!twitch ru`  `twitch th`",
              "`06-Aug-2019`: Added new command    `!protrack HeroName` ",
              "`05-Aug-2019`: Added Notable hero in    `!top game`"]
UPDATE_BLOCK_FOOT = "\nFor more info and support please join: https://discord.gg/a7QYPWd"
LAST_UPDATE = "**UPDATES:**\n" + "\n".join(UPDATE_BLOCK_LIST) + UPDATE_BLOCK_FOOT


# This weird spacing is to pretty text in discord
DOTA_RELATED_COMMAND_LIST = {
                 '!counter HeroName': 'Get counter heroes for given HeroName eg: **`!counter am`**',
                 '!good HeroName'   : 'Opposite of !counter command. Good against. eg: **`!good axe`**',
                 '!skill HeroName': 'Get most popular & win rate talent/skill build  eg:**`!skill meepo`**',
                 '!item HeroName'   : 'Get recent item build by Top Rank Players  eg: **`!item kotl`**',
                 '!trend'           : 'Get current heroes trend  eg: `!trend`',
                 '!agha HeroName': 'Get Aghanim Scepter info for heroes, eg: **`!agha gyro`**',
                 '!meta': 'Get latest hero Meta with MMR brackets  eg: **`!meta`**'
                }

OTHER_COMMAND_LIST = {
    '!guild': 'Managing BOTA in your server',
    '!top game'        : 'Get top 9 Live Games eg: **`!top game`**',
    '!profile  steamID': 'Get your profile stats, Type   **`!profile help`**  for more details',
    '!save steamID': 'Saves your profile steam ID, Type   **`!save help`**  for more details',
    '!twitch language' : 'Get top8 twitch Stream eg:**`!twitch`** **`!twitch en`** **`!twitch ru`**',
    '!reddit': 'Get reddit post from  /r/DotA2. Type **`!reddit help`** for details',
    '!ti': 'Get Group stage Table, TI9 stats,  eg:  `!ti group`,  `!ti stat`',
    '!update': 'Shows any new   `Updates`   and   `BOT support`',
    '!pers': 'Watch Pro Player Perspective @1440p60 `!pers HeroName`'
    }

ADMIN_COMMAND_LIST = {'!stat': 'Shows overall stats and weekly stats',
                       '!stat cmd 14': 'Shows command stats in last 14 days',
                       '!stat new 14': 'Shows new users & servers that joined in last 14 days',
                       '!stat update': 'Update the Log to get latest stats',
                       '!tail': 'Shows last N lines from Log',
                       '!guild': 'Shows total guilds using BOTA',
                       '!loglocal': 'Shows stats and reason if log didnt get push to the log server',
                       '!loglocal clear': 'Clear all local logs',
                       '!broadcast admin_client_id messsage': 'Broadcast Message to servers',
                       '!bglog': 'Tails the background scrap log',
                       '!bglog download': 'Download the background scrap log'}

GUILD_COMMAND_LIST = {'!guild settings': 'Displays current guild settings',
                      '!guild prefix Character': 'Changing the BOTA command prefix of your own choice.\neg: **!guild prefix &**: Prefix change from "!" to "&"',
                      '!guild block ChannelName': 'BOTA will not be able to send  message at ChannelName\neg: **!guild block general**',
                      '!guild unblock general': 'BOTA will be able to send at ChannelName\neg: **!guild unblock general**'}


PROFILE_HELP_STRING = "**To Save your own profile** \n" \
                      "Step 1:   **`!save YourSteamID`**, eg:  **`!save 311360822`**\n" \
                      "Step 2:   **`!profile`** \n" \
                      "Reset :   To reset your SteamID, just type:  **`!save 52870512`**\n\n" \
                      "**To Save someone else profile** \n" \
                      "Step 1:   **`!save Name SteamID`**,  eg: **`!save anna 311360822`** \n" \
                      "Step 2:   **`!profile anna`**\n" \
                      "Reset :   To reset the SteamID for the user you created, type: **`!save anna 52870512`**\n\n" \
                      "**To check profile without saving Steam ID**\n" \
                      "Step 1:   **`!profile SteamID`**,  eg:  **`!profile 311360822`**"

# Team command examples
TEAM_CMD_EXAMPLE = f'**How to use `!team` command**:\n' \
                   f'**`!team HeroName, HeroName, HeroName SkillLevel`**\n\n' \
                   f'**Three skill levels**: `High`, `Normal`, `Low`:\n'\
                   f'eg 1: **`!team lion, am high`**  \n' \
                   f'eg 2: **`!team lion, am normal`**\n' \
                   f'eg 3: **`!team lion, am low`**  \n' \
                   f'eg 4: **`!team lion, am`**'

# Reddit command examples
REDDIT_CMD_EXAMPLE = f'**How to use `!reddit` command**:\n' \
                   f'**`!reddit option`**\n\n' \
                   f'**Options:**: `new`, `controversial`, `top`, `rising`, `hot`\n\n' \
                   f'eg 1: **`!reddit`** \n' \
                   f'eg 2: **`!reddit new`**\n' \
                   f'eg 3: **`!reddit controversial`**\n' \
                   f'eg 4: **`!reddit top`** \n' \
                   f'eg 5: **`!reddit rising`**\n' \
                   f'eg 6: **`!reddit hot`**' \


# COUNTER AND GOOD command examples
COUNTER_EXAMPLE = f'**How to use `!counter` command**:\n' \
                       f'General command: `!counter Heroname` eg: `!counter axe`\n' \
                       f'Alternative command: `!bad Heroname` eg: `!bad axe`\n\n' \
                       f'**Counter a Hero given a specific role:**:\n' \
                       f'Role Options: `mid` `off` `safe` `carry` `support` `inititator` `disabler` `nuker` `pusher`\n' \
                       f'eg 1: **`!counter axe mid`**\n' \
                       f'eg 2: **`!counter am support`**\n' \
                       f'eg 3: **`!counter alchemist safe`**\n' \
                       f'eg 4: **`!counter puck disabler`** or **`!counter puck dis`**\n' \
                       f'eg 5: **`!counter io initiator`** or **`!counter io init`**'

GOOD_EXAMPLE = f'**How to use `!good` command**:\n' \
                       f'General command: `!good Heroname` eg: `!good axe`\n\n' \
                       f'**Counter a Hero given a specific role:**:\n' \
                       f'Role Options: `mid` `off` `safe` `carry` `support` `inititator` `disabler` `nuker` `pusher`\n' \
                       f'eg 1: **`!good axe mid`**\n' \
                       f'eg 2: **`!good am support`**\n' \
                       f'eg 3: **`!good alchemist safe`**\n'\
                       f'eg 4: **`!good puck disabler`** or **`!good puck dis`**\n' \
                       f'eg 5: **`!good io initiator`** or **`!good io init`**'


def get_help(prefix):
    help_string = []
    head = "**Commands to use BOTA**: 😋\n\n"
    # post_head = UPDATE_BLOCK
    # head = head + post_head
    help_string.append(head)
    dota_related_commands = []
    other_commands = []
    for key, value in DOTA_RELATED_COMMAND_LIST.items():
        command = '**' + key.replace('!', prefix) + '**'
        command_help = value.replace('!', prefix)
        full = command + ':' + command_help
        dota_related_commands.append(full + '\n')

    for key, value in OTHER_COMMAND_LIST.items():
        command = '**' + key.replace('!', prefix) + '**'
        command_help = value.replace('!', prefix)
        full = command + ':' + command_help
        other_commands.append(full + '\n')

    dota_related_commands = ''.join(dota_related_commands)
    # dota_related_commands += '\n' + '_'* 2
    other_commands = ''.join(other_commands)
    # other_commands += '\n' + ' ' * 10

    help_string = head
    # print(len(command_string))
    embed_msg = discord.Embed(description=help_string, color=discord.Color.blue())
    embed_msg.set_author(name=constant.DEFAULT_EMBED_HEADER['name'], icon_url=constant.DEFAULT_EMBED_HEADER['icon_url'], url=constant.DEFAULT_EMBED_HEADER['url'])
    embed_msg.set_footer(text=get_random_footer(prefix), icon_url=constant.DOTA2_LOGO_URL)
    embed_msg.add_field(name="Dota Hero Commands", value=dota_related_commands, inline=False)
    embed_msg.add_field(name="Dota Other Commands", value=other_commands, inline=False)
    embed_msg.add_field(name="Help and Support",
                        value=(f"Add BOTA to your server: **[Link]({BOTA_ADD_TO_SERVER_URL})**\n"
                               f"Join BOTA server for more help: **[Link]({BOTA_SUPPORT_SERVER_URL})**\n"
                               f"If you like BOTA do support us to keep the server running: **[Donate]({PAYPAL_URL})**"))
    embed_msg.add_field(name="Updates", value=UPDATE_BLOCK.replace('!', prefix))
    return embed_msg


def get_admin_commands(prefix):
    head = "**Admin  BOTA Commands**:\n\n"
    embed_msg = discord.Embed(description=head, color=discord.Color.blue())
    embed_msg.set_author(name=constant.DEFAULT_EMBED_HEADER['name'], icon_url=constant.DEFAULT_EMBED_HEADER['icon_url'],
                         url=constant.DEFAULT_EMBED_HEADER['url'])
    for key, value in ADMIN_COMMAND_LIST.items():
        key = f"**`{key.replace('!', prefix)}`**"
        embed_msg.add_field(name=key, value=value, inline=True)

    embed_msg.set_footer(text=get_random_footer(prefix), icon_url=constant.DOTA2_LOGO_URL)
    return embed_msg


def get_guild_commands(prefix):
    head = "**Guild Commands**:\n\n"
    embed_msg = discord.Embed(description=head, color=discord.Color.dark_gold())
    embed_msg.set_author(name=constant.DEFAULT_EMBED_HEADER['name'], icon_url=constant.DEFAULT_EMBED_HEADER['icon_url'],
                         url=constant.DEFAULT_EMBED_HEADER['url'])
    for key, value in GUILD_COMMAND_LIST.items():
        key = f"**`{key.replace('!', prefix)}`**"
        embed_msg.add_field(name=key, value=value.replace('!', prefix), inline=False)

    # embed_msg.set_footer(text=HELP_FOOTER, icon_url=constant.DOTA2_LOGO_URL)
    return embed_msg


def pretty_guild_settings(my_dict, head=None, inline=False):
    if head is None:
        head = "**Guild settings**:\n\n"
    embed_msg = discord.Embed(description=head, color=discord.Color.dark_gold())
    embed_msg.set_author(name=constant.DEFAULT_EMBED_HEADER['name'], icon_url=constant.DEFAULT_EMBED_HEADER['icon_url'],
                         url=constant.DEFAULT_EMBED_HEADER['url'])
    for key, value in my_dict.items():
        key = f"**`{key}`**"
        embed_msg.add_field(name=key, value=value, inline=inline)

    # embed_msg.set_footer(text=HELP_FOOTER, icon_url=constant.DOTA2_LOGO_URL)
    return embed_msg

