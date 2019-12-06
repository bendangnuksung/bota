import discord
from bota import  constant

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

# Note
HERO_SHORT_NAME_NOTE = "**NOTE**: Can use short Hero Names, !counter anti mage  !counter am"


# Update Block
# UPDATE_BLOCK = 'Get Synergy hero for team with **`!synergy`**.\nType **`!synergy help`** for details'
UPDATE_BLOCK = 'Command available for heroes Snapfire & Void Spirit, type `!counter snapfire`  `!item void spirit`'


UPDATE_BLOCK_LIST=\
             ["`30-Sep-2019`: Added Aghanim Info for heroes, type `!agha HeroName`",
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
                 '!team HeroName': 'Getnext best hero for team. Type:**`!team help`** for details',
                 '!item HeroName'   : 'Get recent item build by Top Rank Players  eg: **`!item kotl`**',
                 '!trend'           : 'Get current heroes trend  eg: `!trend`',
                 '!pro HeroName': 'Hero recently played by Pros and stats. eg:**`!protrack slark`**',
                 '!agha HeroName': 'Get Aghanim Scepter info for heroes, eg: **`!agha gyro`**'
                }

OTHER_COMMAND_LIST = {
    '!top game'        : 'Get top 9 Live Games eg: **`!top game`**',
    '!profile  steamID': 'Get your profile stats, Type   **`!profile help`**  for more details',
    '!save steamID': 'Saves your profile steam ID, Type   **`!save help`**  for more details',
    '!twitch language' : 'Get top8 twitch Stream eg:**`!twitch`** **`!twitch en`** **`!twitch ru`**',
    '!reddit': 'Get reddit post from  /r/DotA2. Type **`!reddit help`** for details',
    '!ti': 'Get Group stage Table, TI9 stats,  eg:  `!ti group`,  `!ti stat`',
    '!update': 'Shows any new   `Updates`   and   `BOT support`'
    }


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


def get_help():
    help_string = []
    head = "**Commands to use BOTA**: 😋\n\n"
    # post_head = UPDATE_BLOCK
    # head = head + post_head
    help_string.append(head)
    dota_related_commands = []
    other_commands = []
    for key, value in DOTA_RELATED_COMMAND_LIST.items():
        command = '**' + key + '**'
        command_help = value
        full = command + ':' + command_help
        dota_related_commands.append(full + '\n')

    for key, value in OTHER_COMMAND_LIST.items():
        command = '**' + key + '**'
        command_help = value
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
    embed_msg.set_footer(text=HELP_FOOTER, icon_url=constant.DOTA2_LOGO_URL)
    embed_msg.add_field(name="Dota Hero Commands", value=dota_related_commands, inline=False)
    embed_msg.add_field(name="Dota Other Commands", value=other_commands, inline=False)
    embed_msg.add_field(name="Help and Support",
                        value=(f"Add BOTA to your server: **[Link]({BOTA_ADD_TO_SERVER_URL})**\n"
                               f"Join BOTA server for more help: **[Link]({BOTA_SUPPORT_SERVER_URL})**\n"
                               f"If you like BOTA do support us to keep the server running: **[Donate]({PAYPAL_URL})**"))
    embed_msg.add_field(name="Updates", value=UPDATE_BLOCK)
    return embed_msg
