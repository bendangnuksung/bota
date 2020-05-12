import os
import requests

# Private keys
DISCORD_TOKEN = ""
DOTA2_API_KEY = ""
DISCORD_CLIENT_ID = ""
ADMIN_ID = "" # Discord User
TWITCH_CLIENT_IDS = [] # List of strings: twitch client IDs
TWITCH_SECRET_KEY = []
LOG_PORCESS_IP_ADDRESS = '' #  IP address with Port Number where the LOG will be processed (Not necessary)


def get_steam_auth_token(client_id, secret_id):
    url = f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={secret_id}&grant_type=client_credentials'
    r = requests.post(url)
    r = r.json()
    token = r['access_token']
    return token


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

if len(TWITCH_CLIENT_IDS) <= 0:
    twitch = env_var.get('TWITCH_CLIENT_IDS')
    TWITCH_CLIENT_IDS = [env_var.get('TWITCH_CLIENT_IDS')]
    if TWITCH_CLIENT_IDS is None:
        print("TWITCH_CLIENT_IDS not provided")

if len(TWITCH_SECRET_KEY) <= 0:
    twitch = env_var.get('TWITCH_SECRET_KEY')
    TWITCH_SECRET_KEY = [env_var.get('TWITCH_SECRET_KEY')]
    if TWITCH_SECRET_KEY is None:
        print("TWITCH SECRET KEY not provided")

if LOG_PORCESS_IP_ADDRESS == "":
    LOG_PORCESS_IP_ADDRESS = env_var.get('LOG_PORCESS_IP_ADDRESS')
    if LOG_PORCESS_IP_ADDRESS is None:
        LOG_PORCESS_IP_ADDRESS = 'http://0.0.0.0:5000/'
        print("LOG_PORCESS_IP_ADDRESS not provided, taking default address")


CREDS = {'Discord Token': DISCORD_TOKEN, 'Discord Client ID': DISCORD_CLIENT_ID, 'DOTA2 APIKEY':DOTA2_API_KEY,
         'Admin ID': ADMIN_ID, 'Twitch Client IDs': TWITCH_CLIENT_IDS, 'Log IP address':LOG_PORCESS_IP_ADDRESS}
print("*"*40)
print("CREDENTIALS")
for key, val in CREDS.items():
    print(key, ': ', val)
print("*"*40)


TWITCH_AUTH_TOKENS = {}
for client_id, secret_key in zip(TWITCH_CLIENT_IDS, TWITCH_SECRET_KEY):
    oth_token = get_steam_auth_token(client_id, secret_key)
    TWITCH_AUTH_TOKENS[client_id] = oth_token
