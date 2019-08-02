from bota.private_constant import DISCORD_TOKEN, DOTA2_API_KEY, DISCORD_CLIENT_ID, TWITCH_CLIENT_IDS
import sys


IS_BOTA_READY = True
REASON = "Key value missing in 'bota/private_constant.py':\n"

# Check all keys are present
if DISCORD_TOKEN == "":
    IS_BOTA_READY = False
    REASON += "Discord Token: Empty\n"

if DOTA2_API_KEY == "":
    IS_BOTA_READY = False
    REASON += "Dota2 Api Key: Empty\n"

if DISCORD_CLIENT_ID == "":
    IS_BOTA_READY = False
    REASON += "Discord Client ID: Empty\n"

if len(TWITCH_CLIENT_IDS) == 0:
    IS_BOTA_READY = False
    REASON += "Twitch Client ID: Empty\n"


if IS_BOTA_READY:
    sys.exit(0)
else:
    print(REASON)
    sys.exit(1)