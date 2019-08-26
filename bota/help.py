HOW_TO_USE_COMMANDS_EXAMPLE = {
    '!profile': 'How to use:\n1. With SteamID:  `!profile 116585378`\n2. With Name: !profile midone`  (Save your name using `!save` command)`',
    '!save': 'How to use -> `!save midone 116585378`',
    '!counter': 'How to use -> `!counter axe`  `!counter zeus`',
    '!good': 'How to use -> `!good am`  `!good jugg`',
    '!skill': 'How to use -> `!skill phoenix`  `!good sf`',
    '!item': 'How to use -> `!item meepo`  `!item et`',
    '!twitch': 'How to use:\n `!twitch`   `!twitch en`   `!twitch ru`   `!twitch russian',
    '!reddit': 'How to use:\n 1. `!reddit`\n2. `!reddit hot`\n3. `!reddit new',
    '!pro': 'How to use:  `!pro slark`   `!pro meepo`'
    }

# Foot block
HELP_FOOTER = "**NOTE**: Can use short Hero Names, !counter anti mage ---as---> !counter am"

# Note
HERO_SHORT_NAME_NOTE = "**NOTE**: Can use short Hero Names, !counter anti mage  !counter am"


# Update Block
UPDATE_BLOCK = '```cs\n"UPDATE": Can save your profile without name and change Steam ID and others, Type "!profile help" for details```'
LAST_UPDATE = "**UPDATES:**\n" \
              "1. Added TI command,   `!ti`   date: `15-Aug-2019`\n" \
              "2. Added Language option in twitch    `!twitch en`    date: `07-Aug-2019`\n"\
              "3. Added new command    `!protrack HeroName`    date: `06-Aug-2019`\n" \
              "4. Added Notable hero in    `!top game`    date: `05-Aug-2019`\n" \
              "For more info and support please join: https://discord.gg/a7QYPWd"


# This weird spacing is to pretty text in discord
COMMAND_LIST = {'!top game'        : 'Shows top 9 Live Games eg: **`!top game`**',
                 '!counter HeroName': 'Show Heroes that counter given HeroName eg: **`!counter am`**',
                 '!good HeroName'   : 'Opposite of !counter command. Good against. eg: **`!good axe`**',
                 '!skill': 'Shows most popular & win rate talent/skill build  eg:**`!skill meepo`**',
                 '!item HeroName'   : 'Shows recent item build by Top Rank Players  eg: **`!item kotl`**',
                 '!profile  steamID': 'Shows your profile stats, Type   **`!profile help`**  for more details',
                 '!save steamID': 'Saves your profile steam ID, Type   **`!save help`**  for more details',
                 '!trend'           : 'Shows current heroes trend  eg: `!trend`',
                 '!twitch language' : 'Show top8 twitch Stream eg:**`!twitch`** **`!twitch en`** **`!twitch ru`**',
                 '!pro HeroName': 'Hero recently played by Pros and stats. eg:**`!protrack slark`**',
                 '!ti': 'Shows Group stage Table, TI9 stats,  eg:  `!ti group`,  `!ti stat`',
                 '!reddit'          : 'Gets reddit post from   **/r/DotA2**. Options: `new`, `controversial`, `top`, `rising`, `random`, `hot`:\n'
                                      '                       eg 1:   **`!reddit`** : Gets a random post from  /r/DotA2/\n'
                                      '                       eg 2:   **`!reddit hot`** : Gets Top 3 hot post from  /r/DotA2/',
                 '!update'     : 'Shows any new   `Updates`   and   `BOT support`'
                }


def get_help():
    help_string = []
    head = "```css\nBelow are the commands to use DOTA BOT: 😋```"
    post_head = UPDATE_BLOCK
    head = head + post_head
    help_string.append(head)
    body = []
    for key, value in COMMAND_LIST.items():
        command = '**' + key + '**'
        command_help = value
        full = command + '\t:\t' + command_help
        body.append(full + '\n')
    help_string = help_string + body
    help_string = "\n".join(help_string)
    return help_string


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
