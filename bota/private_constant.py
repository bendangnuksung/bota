import os

# Private keys
DISCORD_TOKEN = ""
DOTA2_API_KEY = ""
DISCORD_CLIENT_ID = ""
ADMIN_ID = "" # Discord User
TWITCH_CLIENT_IDS = [] # List of strings: twitch client IDs
LOG_PORCESS_IP_ADDRESS = 'localhost' # IP addres where the LOG will be processed (Not necessary)


# Take keys from environment variable if empty
env_var = os.environ
if DISCORD_TOKEN == "":
    DISCORD_TOKEN = env_var.get('DISCORD_TOKEN')
    if DISCORD_TOKEN is None:
        print("DISCORD_TOKEN not provided")

if DOTA2_API_KEY == "":
    DOTA2_API_KEY = env_var.get('DOTA2_API_KEY')
    if DOTA2_API_KEY is None:
        print("DOTA2_API_KEY not provided")

if DISCORD_CLIENT_ID == "":
    DISCORD_CLIENT_ID = env_var.get('DISCORD_CLIENT_ID')
    if DISCORD_CLIENT_ID is None:
        print("DISCORD_CLIENT_ID not provided")

if ADMIN_ID == "":
    ADMIN_ID = env_var.get('ADMIN_ID')
    if ADMIN_ID is None:
        print("ADMIN_ID not provided")

if TWITCH_CLIENT_IDS == "":
    TWITCH_CLIENT_IDS = env_var.get('TWITCH_CLIENT_IDS')
    if TWITCH_CLIENT_IDS is None:
        print("TWITCH_CLIENT_IDS not provided")

if LOG_PORCESS_IP_ADDRESS == "":
    LOG_PORCESS_IP_ADDRESS = env_var.get('LOG_PORCESS_IP_ADDRESS')
    if LOG_PORCESS_IP_ADDRESS is None:
        print("LOG_PORCESS_IP_ADDRESS not provided")
