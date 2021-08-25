import os


YOUTUBE_CHANNEL_URL = "https://www.youtube.com/channel/UCnby5VqRpcJ-qzyhAp2cTAQ"

# command prefix
DEFAULT_PREFIX = '!'

BOTA_LOGO_URL = 'https://raw.githubusercontent.com/bendangnuksung/bota/master/github_images/bota.png'

# General
MAX_COMMAND_WORD_LENGTH = 5
REPO_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_EMBED_HEADER = {'name': 'Bota', 'icon_url': 'https://raw.githubusercontent.com/bendangnuksung/bota/master/github_images/bota.png',
                        'url': 'https://bota.tech'}
DOTA2_LOGO_URL = 'https://seeklogo.com/images/D/dota-2-logo-A8CAC9B4C9-seeklogo.com.png'
CHARACTER_ICONS_URL ='https://raw.githubusercontent.com/bendangnuksung/bota/master/bota/data/character_icons_big/'

# Early Update time (Scrap data early by Threshold time i.e THRESHOLD_UPDATE_TIME - EARLY_BY )
EARLY_BY = 3600 # Hour, Update early by an hour

# TI9
TI_LOGO_URL = 'https://liquipedia.net/commons/images/thumb/f/fc/Ti9_teamcard_logo.png/147px-Ti9_teamcard_logo.png'


# Profile Info
PLAYER_URL_BASE = 'https://www.dotabuff.com/players/'

# Steam User json file
STEAM_USER_FILE_PATH = 'data/steam_user/steam_user.json'
STEAM_USER_FILE_PATH = os.path.join(REPO_PATH, STEAM_USER_FILE_PATH)
NEW_USER_FILE_PATH_CSV = 'data/steam_user/new_steam_user.csv'
NEW_USER_FILE_PATH_CSV = os.path.join(REPO_PATH, NEW_USER_FILE_PATH_CSV)

# Log path
COMMAND_USER_LOG_PATH = "data/logs/command_user_log.txt"
COMMAND_USER_LOG_PATH = os.path.join(REPO_PATH, COMMAND_USER_LOG_PATH)
SCRAP_LOG_PATH = 'data/logs/scrap_log.txt'
SCRAP_LOG_PATH = os.path.join(REPO_PATH, SCRAP_LOG_PATH)

# yt link path
YT_LINK_PATH = os.path.join(REPO_PATH, 'data/logs/youtube_links.json')
ALL_YT_LINK_PATH = os.path.join(REPO_PATH, 'data/logs/all_youtube_links.json')
YT_GIST_ID = "7feeb3f31eb81c78db1b3edf3ae1b0c2"


# Dota 2 ProTracker
D2PT_HERO_UPDATE_THRESHOLD = 600 # 10 min
D2PT_WEBSITE_URL = 'http://www.dota2protracker.com/'
D2PT_URL_LIVE_GAMES = "http://www.dota2protracker.com/livegames"
D2PT_HERO_BASE_URL = 'http://dota2protracker.com/api/hero/'
D2PT_KEYWORD_META = 'meta'
D2PT_KEYWORD_CROSS_META = 'cross_meta'
D2PT_KEYWORD_RECENT_MATCH = 'recent_matches'
D2PT_KEYWORD_GOOD_AGAINST = 'best_versus'
D2PT_KEYWORD_BAD_AGAINST = 'worst_versus'

WANTED_KEYS_RECENT_MATCHES = ['pro', 'matchid', 'won', 'time']
RECENT_MATCHES_KEY_RENAME = {'pro': 'name', 'time': 'played', 'won': 'w/l'}

WANTED_KEYS_GOOD_AGAINST = ['name', 'won_against', 'lost_against']
WANTED_KEYS_BAD_AGAINST = ['name', 'won_against', 'lost_against']



# Reddit
REDDIT_DOTA_URL = 'https://www.reddit.com/r/DotA2/'
REDDIT_SORT_BY = ['new', 'controversial', 'top', 'rising', 'random', 'hot']
REDDIT_SORT_BY_REFRESH_SEC = {'new': 5, 'controversial': 60, 'top': 300, 'rising': 60, 'random': 5, 'hot': 60}
REDDIT_DEFAULT_MODE = 'random'
REDDIT_DEFAULT_TOP = 3
REDDIT_MAX_POST_LIMIT = 6

JSON_POSTFIX = '.json'
REDDIT_URL = 'https://www.reddit.com'
REDDIT_POST_BODY = 'selftext'
REDDIT_POST_TITLE = 'title'
REDDIT_POST_AUTHOR = 'author'
REDDIT_POST_FLAIR = 'link_flair_text'
REDDIT_POST_SCORE = 'score'
REDDIT_POST_URL = 'permalink'
REDDIT_POST_MEDIA_URL = 'url'
REDDIT_BODY_MAX_CHARACTER = 300
WEBPAGE_PRE_STRING = ['https://', 'http://']


# Twitch
DOTA_2_GAME_ID = '29595'
TWITCH_URL = 'https://www.twitch.tv/'
TWITCH_DOTA_2_STREAM_URL = 'https://api.twitch.tv/helix/streams?game_id='

TWITCH_KEYWORD_CLIENT_ID = 'client-id'
TWITCH_KEYWORD_USER_NAME = 'user_name'
TWITCH_KEYWORD_DATA = 'data'
TWITCH_KEYWORD_VIEWER_COUNT = 'viewer_count'
TWITCH_KEYWORD_TITLE = 'title'
TWITCH_KEYWORD_LANGUAGE = 'language'


TEMP_IMAGE_PATH = 'data/temp_images'
TEMP_IMAGE_PATH = os.path.join(REPO_PATH, TEMP_IMAGE_PATH)


DOTABUFF_URL = 'https://www.dotabuff.com'
DOTABUFF_PLAYER_URL = 'https://www.dotabuff.com/players/'
DOTABUFF_ITEM_IMAGE_URL = 'https://www.dotabuff.com/assets/items/'

FONT_ROBOTO_PATH = os.path.join(REPO_PATH, 'font/Roboto-Regular.ttf')

# icon Path
ICON_PATH_SMALL = 'data/character_icons/'
ICON_PATH_BIG   = 'data/character_icons_big/'
ICON_PATH_SMALL = os.path.join(REPO_PATH, ICON_PATH_SMALL)
ICON_PATH_BIG   = os.path.join(REPO_PATH, ICON_PATH_BIG)

ITEM_ICON_PATH = 'data/items'
ITEM_ICON_PATH = os.path.join(REPO_PATH, ITEM_ICON_PATH)


# Medals
MEDAL_IMAGE_PATH = 'data/medals'
MEDAL_IMAGE_PATH = os.path.join(REPO_PATH, MEDAL_IMAGE_PATH)
MEDAL_NAMES = ['immortal', 'divine', 'ancient', 'legend', 'archon', 'crusader', 'guardian', 'herald', 'uncalibrated']
MEDAL_IMMORTAL_UNDER = {5000: 'immortal.png', 100: 'immortal-100.png', 10:'immortal-10.png'}
MEDAL_NUMBERING = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7,
				   '1': 1, '2': 2,  '3': 3,    '4': 4, '5': 5, '6': 6,   '7': 7}
MEDAL_SHAPE = [85, 85]

MEDAL_RANK_START_X_Y_PERCENTAGE = [.70, .30]

MEDAL_ITEM_X_Y = [50, 90]
MEDAL_ITEM_HEIGHT_DIFF = 100


# Meta
META_URL = 'https://www.dotabuff.com/heroes/meta'
META_THRESHOLD_UPDATE = 6000
META_IMAGE_PATH = 'data/temp_images/meta.jpg'
META_IMAGE_PATH = os.path.join(REPO_PATH, META_IMAGE_PATH)
META_TEMPLATE_IMAGE = 'data/template_image/meta_template.png'
META_TEMPLATE_IMAGE = os.path.join(REPO_PATH, META_TEMPLATE_IMAGE)
META_OFFSET_X = 0
META_OFFSET_Y = -65
META_OFFSET_HEIGHT = 780
META_OFFSET_WIDTH = 1170

META_HERO_SPLIT_1_COORDS = [0, 0, 55, -1] # xmin,ymin,xmax,ymax
META_HERO_SPLIT_2_COORDS = [265, 0, -1, -1] # xmin,ymin,xmax,ymax


# Item Guide
ITEM_IMAGE_PATH = 'data/items_build/'
ITEM_IMAGE_PATH = os.path.join(REPO_PATH, ITEM_IMAGE_PATH)
ITEM_URL = 'https://www.dotabuff.com/heroes/<hero_name>/guides'

ITEM_BACKGROUND_IMAGE = 'data/background/items_background.jpg'
ITEM_BACKGROUND_IMAGE = os.path.join(REPO_PATH, ITEM_BACKGROUND_IMAGE)
ITEM_BACKGROUND_IMAGE_SHAPE = [600, 1070+440]

ITEM_THRESHOLD_UPDATE = 43200 # 12 hour

ITEM_FIRST_STAGE_TAG = ['div', {'class': 'r-stats-grid'}]
ITEM_PLAYER_NAME_ID_TAG = ['div', {'class': 'kv kv-larger kv-small-margin'}]
ITEM_BUILD_TAG = ["div", {"class": "top-right"}]
ITEM_MATCH_ID_TAG = ['a', {'class': 'button button-small'}]
ITEM_BUILD_TIME_TAG = ['div', {'class': 'time time-below'}]
ITEM_BUILD_ITEM_TAG = ['img', {'class': 'image-item image-medicon'}]
ITEM_PLAYER_RANK_INFO_TAG = ['div', {'class': 'rank-tier-wrapper'}]
ITEM_REGION_FIRST_TAG = ['div', {'class': 'kv kv-label'}]
ITEM_REGION_FIRST_TAG_CHILD_NO = 4

ITEM_KEYWORD_REGION = 'region'
ITEM_KEYWORD_ITEM_BUILD = 'item_build'
ITEM_KEYWORD_PLAYER_ID = 'player_id'
ITEM_KEYWORD_MATCH_ID = 'match_id'
ITEM_KEYWORD_PLAYER_NAME = 'player_name'
ITEM_KEYWORD_TITLE = 'title'
ITEM_KEYWORD_ITEM = 'item'
ITEM_KEYWORD_TIME_TAKEN = 'time'
ITEM_KEYWORD_RANK = 'rank'
ITEM_KEYWORD_RANK_MEDAl = 'medal'

ITEM_TOP_PLAYERS_MEDALS = ['immortal', 'divine']

MAX_ITEM = 6

MAX_CHAR_PLAYER_NAME = 10
MAX_CHAR_REGION      = 8

PLAYER_NAME_FONT_SIZE = 25
PLAYER_ID_FONT_SIZE   = 25
MATCH_ID_FONT_SIZE    = 25
REGION_FONT_SIZE      = 25
TIME_FONT_SIZE = 18

PLAYER_NAME_START_LEFT = 160
PLAYER_ID_START_LEFT   = 330
PLAYER_MATCH_ID_START_LEFT = 310
REGION_START_LEFT      = 480
ITEM_START_LEFT = 600
TIME_START_TOP = -10


ITEM_RANK_PRE_CHAR = '#'

ITEM_WRITE_PLAYER_NAME_X_Y = []

ITEM_ICON_SHAPE = (68, 45)

ITEM_HERO_ICON_PLACEMENT_TOP = 5
ITEM_HERO_ICON_PLACEMENT_LEFT = 30


# Talent, Skill screenshot coords, matchID
GUIDE_BACKGROUND_PATH = 'data/background/build_background.jpg'
GUIDE_BACKGROUND_SHAPE = [80, 800]
GUIDE_HERO_ICON_X_Y = [4, 336]
GUIDE_BACKGROUND_PATH = os.path.join(REPO_PATH, GUIDE_BACKGROUND_PATH)
GUIDE_THRESHOLD_IMAGE_UPDATE = 43200 # 12 hour
GUIDE_SAVE_PATH = 'data/guide_build'
GUIDE_SAVE_PATH = os.path.join(REPO_PATH, GUIDE_SAVE_PATH)

GUIDE_URL_TALENT = 'https://www.dotabuff.com/heroes/<hero_name>/builds'
TALENT_SELECTOR = 'body > div.container-outer.seemsgood > div.skin-container > div.container-inner.container-inner-content > div.content-inner > div.row-12.hero-abilities > div.col-8 > section:nth-child(1) > article'
TALENT_TEMPLATE_PATH = 'data/template_image/talent_build_template.png'
TALENT_TEMPLATE_PATH = os.path.join(REPO_PATH, TALENT_TEMPLATE_PATH)
TALENT_OFFSET_X = 40
TALENT_OFFSET_Y = 0
TALENT_OFFSET_HEIGHT = 342
TALENT_OFFSET_WIDTH = 660

GUIDE_URL_SKILL = 'https://www.dotabuff.com/heroes/<hero_name>'
SKILL_SELECTOR = 'body > div.container-outer.seemsgood > div.skin-container > div.container-inner.container-inner-content > div.content-inner > div:nth-child(2) > div:nth-child(5) > div.build'
SKILL_TEMPLATE_PATH = 'data/template_image/skill_build_template.png'
SKILL_TEMPLATE_PATH = os.path.join(REPO_PATH, SKILL_TEMPLATE_PATH)
SKILL_OFFSET_X = 0
SKILL_OFFSET_Y = 0
SKILL_OFFSET_HEIGHT = 245
SKILL_OFFSET_WIDTH = 652


# Counter Hero
COUNTER_HERO_IMAGE_PATH = 'data/counter_heroes/'
COUNTER_HERO_IMAGE_PATH = os.path.join(REPO_PATH, COUNTER_HERO_IMAGE_PATH)
COUNTER_HERO_UPDATE_TIME_THRESHOLD = 43200 # 12 hour
COUNTER_BG_IMAGE_PATH = 'data/background/counter_backgound.jpg'
COUNTER_BG_IMAGE_PATH = os.path.join(REPO_PATH, COUNTER_BG_IMAGE_PATH)
COUNTER_BG_SHAPE = (400, 800)
COUNTER_ICON_SHAPE = (60, 96)
COUNTER_MAIN_HERO_COORDS = [305, 340]
COUNTER_START_COORDS = [25, 70]
COUNTER_WIDTH_DIST = 30
COUNTER_HEIGHT_DIST = 100
COUNTER_MAX_COLUMN = 5

# Hero Good against
GOOD_HERO_UPDATE_TIME_THRESHOLD = 43200 # 12 hour
GOOD_HERO_IMAGE_PATH = 'data/good_against_heroes/'
GOOD_HERO_IMAGE_PATH = os.path.join(REPO_PATH, GOOD_HERO_IMAGE_PATH)
GOOD_BG_IMAGE_PATH = 'data/background/good_against_background.jpg'
GOOD_BG_IMAGE_PATH = os.path.join(REPO_PATH, GOOD_BG_IMAGE_PATH)

# Current Trend
CT_IMAGE_PATH = 'data/temp_images/current_trend.png'
CT_IMAGE_PATH = os.path.join(REPO_PATH, CT_IMAGE_PATH)
CT_IMAGE_UPDATE_TIME_THRESHOLD = 7200 # 2 hour

# top live game
TLG_IMAGE_PATH = 'data/temp_images/top_live_games.png'
TLG_IMAGE_PATH = os.path.join(REPO_PATH, TLG_IMAGE_PATH)
TLG_IMAGE_UPDATE_TIME_THRESHOLD = 10 # 10 sec

TLG_CUSTOM_COLUMNS = ['Radiant', 'Dire', 'Avg MMR', 'Game Mode',
					  'Spectators', 'Time', 'R Kills', 'D Kills', 'Gold Lead']
KEYWORD_AVERAGE_MMR = 'average_mmr'
KEYWORD_GAME_MODE = 'game_mode'
KEYWORD_GAME_TIME = 'game_time'
KEYWORD_SPECTATORS = 'spectators'
KEYWORD_RADIANT_LEAD = 'radiant_lead'
KEYWORD_RADIANT_SCORE = 'radiant_score'
KEYWORD_DIRE_SCORE = 'dire_score'
KEYWORD_RADIANT_TEAM = 'team_name_radiant'
KEYWORD_DIRE_TEAM = 'team_name_dire'
KEYWORD_MATCH_ID = "match_id"

# Dotavoyance Contants
DV_DEFAULT_IMAGE_WIDTH = 1024
DV_DEFAULT_IMAGE_HEIGHT = 1024 #768
DV_NUM_CHANNELS = 4
DV_HEIGHT_BUFFER = 10
DV_COLUMN_BUFFER = 10
DV_ICON_URL = 'https://pbs.twimg.com/profile_images/1074104310550679552/WZmQbyIP.jpg'
DV_SITE_HOME = 'https://www.dotavoyance.com/'
DV_SITE_TEAM_URL = 'https://www.dotavoyance.com/heroteammates'
DV_TEAM_IMAGE_PATH = 'data/team_heroes/'
DV_TEAM_IMAGE_PATH = os.path.join(REPO_PATH, DV_TEAM_IMAGE_PATH)
DV_TEAM_BG_IMAGE = 'data/background/team_background.jpg'
DV_TEAM_BG_IMAGE = os.path.join(REPO_PATH, DV_TEAM_BG_IMAGE)
DV_TEAM_BG_IMAGE_WITHOUT_WINRATE = 'data/background/team_background_no_winrate.jpg'
DV_TEAM_BG_IMAGE_WITHOUT_WINRATE = os.path.join(REPO_PATH, DV_TEAM_BG_IMAGE_WITHOUT_WINRATE)

# Dota 2 API constant
rank_tier = ['herald', 'Guardian', 'Crusader', 'Archon','Legend', 'Ancient','Divine', 'Immortal']

GAME_MODE = {0 :'Unknown', 				1:'All Pick', 			2:'Captain’s Mode', 		3:'Random Draft',
			 4:'Single Draft', 			5:'All Random',			6:'Intro', 					7:'Diretide',
			 8:'Reverse Captain’s Mode',9:'The Greeviling', 	10:'Tutorial', 				11:'Mid Only',
			 12:'Least Played', 		13:'New Player Pool', 	14:'Compendium Matchmaking',15:'Custom',
			 16:'Captains Draft',		17:'Balanced Draft',    18:'Ability Draft', 		19:'Event (?)',
			 20:'All Random Death Match',21:'Solo Mid 1 vs 1',  22:'Ranked All Pick'}


COUNTRIES = {
	'AF': 'AFGHANISTAN',
	'AX': 'ÅLAND ISLANDS',
	'AL': 'ALBANIA',
	'DZ': 'ALGERIA',
	'AS': 'AMERICAN SAMOA',
	'AD': 'ANDORRA',
	'AO': 'ANGOLA',
	'AI': 'ANGUILLA',
	'AQ': 'ANTARCTICA',
	'AG': 'ANTIGUA AND BARBUDA',
	'AR': 'ARGENTINA',
	'AM': 'ARMENIA',
	'AW': 'ARUBA',
	'AU': 'AUSTRALIA',
	'AT': 'AUSTRIA',
	'AZ': 'AZERBAIJAN',
	'BS': 'BAHAMAS',
	'BH': 'BAHRAIN',
	'BD': 'BANGLADESH',
	'BB': 'BARBADOS',
	'BY': 'BELARUS',
	'BE': 'BELGIUM',
	'BZ': 'BELIZE',
	'BJ': 'BENIN',
	'BM': 'BERMUDA',
	'BT': 'BHUTAN',
	'BO': 'BOLIVIA, PLURINATIONAL STATE OF',
	'BQ': 'BONAIRE, SINT EUSTATIUS AND SABA',
	'BA': 'BOSNIA AND HERZEGOVINA',
	'BW': 'BOTSWANA',
	'BV': 'BOUVET ISLAND',
	'BR': 'BRAZIL',
	'IO': 'BRITISH INDIAN OCEAN TERRITORY',
	'BN': 'BRUNEI DARUSSALAM',
	'BG': 'BULGARIA',
	'BF': 'BURKINA FASO',
	'BI': 'BURUNDI',
	'KH': 'CAMBODIA',
	'CM': 'CAMEROON',
	'CA': 'CANADA',
	'CV': 'CAPE VERDE',
	'KY': 'CAYMAN ISLANDS',
	'CF': 'CENTRAL AFRICAN REPUBLIC',
	'TD': 'CHAD',
	'CL': 'CHILE',
	'CN': 'CHINA',
	'CX': 'CHRISTMAS ISLAND',
	'CC': 'COCOS (KEELING) ISLANDS',
	'CO': 'COLOMBIA',
	'KM': 'COMOROS',
	'CG': 'CONGO',
	'CD': 'CONGO, THE DEMOCRATIC REPUBLIC OF THE',
	'CK': 'COOK ISLANDS',
	'CR': 'COSTA RICA',
	'CI': 'CÔTE D\'IVOIRE',
	'HR': 'CROATIA',
	'CU': 'CUBA',
	'CW': 'CURAÇAO',
	'CY': 'CYPRUS',
	'CZ': 'CZECH REPUBLIC',
	'DK': 'DENMARK',
	'DJ': 'DJIBOUTI',
	'DM': 'DOMINICA',
	'DO': 'DOMINICAN REPUBLIC',
	'EC': 'ECUADOR',
	'EG': 'EGYPT',
	'SV': 'EL SALVADOR',
	'GQ': 'EQUATORIAL GUINEA',
	'ER': 'ERITREA',
	'EE': 'ESTONIA',
	'ET': 'ETHIOPIA',
	'FK': 'FALKLAND ISLANDS (MALVINAS)',
	'FO': 'FAROE ISLANDS',
	'FJ': 'FIJI',
	'FI': 'FINLAND',
	'FR': 'FRANCE',
	'GF': 'FRENCH GUIANA',
	'PF': 'FRENCH POLYNESIA',
	'TF': 'FRENCH SOUTHERN TERRITORIES',
	'GA': 'GABON',
	'GM': 'GAMBIA',
	'GE': 'GEORGIA',
	'DE': 'GERMANY',
	'GH': 'GHANA',
	'GI': 'GIBRALTAR',
	'GR': 'GREECE',
	'GL': 'GREENLAND',
	'GD': 'GRENADA',
	'GP': 'GUADELOUPE',
	'GU': 'GUAM',
	'GT': 'GUATEMALA',
	'GG': 'GUERNSEY',
	'GN': 'GUINEA',
	'GW': 'GUINEA-BISSAU',
	'GY': 'GUYANA',
	'HT': 'HAITI',
	'HM': 'HEARD ISLAND AND MCDONALD ISLANDS',
	'VA': 'HOLY SEE (VATICAN CITY STATE)',
	'HN': 'HONDURAS',
	'HK': 'HONG KONG',
	'HU': 'HUNGARY',
	'IS': 'ICELAND',
	'IN': 'INDIA',
	'ID': 'INDONESIA',
	'IR': 'IRAN, ISLAMIC REPUBLIC OF',
	'IQ': 'IRAQ',
	'IE': 'IRELAND',
	'IM': 'ISLE OF MAN',
	'IL': 'ISRAEL',
	'IT': 'ITALY',
	'JM': 'JAMAICA',
	'JP': 'JAPAN',
	'JE': 'JERSEY',
	'JO': 'JORDAN',
	'KZ': 'KAZAKHSTAN',
	'KE': 'KENYA',
	'KI': 'KIRIBATI',
	'KP': 'KOREA, DEMOCRATIC PEOPLE\'S REPUBLIC OF',
	'KR': 'KOREA, REPUBLIC OF',
	'KW': 'KUWAIT',
	'KG': 'KYRGYZSTAN',
	'LA': 'LAO PEOPLE\'S DEMOCRATIC REPUBLIC',
	'LV': 'LATVIA',
	'LB': 'LEBANON',
	'LS': 'LESOTHO',
	'LR': 'LIBERIA',
	'LY': 'LIBYAN ARAB JAMAHIRIYA',
	'LI': 'LIECHTENSTEIN',
	'LT': 'LITHUANIA',
	'LU': 'LUXEMBOURG',
	'MO': 'MACAO',
	'MK': 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF',
	'MG': 'MADAGASCAR',
	'MW': 'MALAWI',
	'MY': 'MALAYSIA',
	'MV': 'MALDIVES',
	'ML': 'MALI',
	'MT': 'MALTA',
	'MH': 'MARSHALL ISLANDS',
	'MQ': 'MARTINIQUE',
	'MR': 'MAURITANIA',
	'MU': 'MAURITIUS',
	'YT': 'MAYOTTE',
	'MX': 'MEXICO',
	'FM': 'MICRONESIA, FEDERATED STATES OF',
	'MD': 'MOLDOVA, REPUBLIC OF',
	'MC': 'MONACO',
	'MN': 'MONGOLIA',
	'ME': 'MONTENEGRO',
	'MS': 'MONTSERRAT',
	'MA': 'MOROCCO',
	'MZ': 'MOZAMBIQUE',
	'MM': 'MYANMAR',
	'NA': 'NAMIBIA',
	'NR': 'NAURU',
	'NP': 'NEPAL',
	'NL': 'NETHERLANDS',
	'NC': 'NEW CALEDONIA',
	'NZ': 'NEW ZEALAND',
	'NI': 'NICARAGUA',
	'NE': 'NIGER',
	'NG': 'NIGERIA',
	'NU': 'NIUE',
	'NF': 'NORFOLK ISLAND',
	'MP': 'NORTHERN MARIANA ISLANDS',
	'NO': 'NORWAY',
	'OM': 'OMAN',
	'PK': 'PAKISTAN',
	'PW': 'PALAU',
	'PS': 'PALESTINIAN TERRITORY, OCCUPIED',
	'PA': 'PANAMA',
	'PG': 'PAPUA NEW GUINEA',
	'PY': 'PARAGUAY',
	'PE': 'PERU',
	'PH': 'PHILIPPINES',
	'PN': 'PITCAIRN',
	'PL': 'POLAND',
	'PT': 'PORTUGAL',
	'PR': 'PUERTO RICO',
	'QA': 'QATAR',
	'RE': 'RÉUNION',
	'RO': 'ROMANIA',
	'RU': 'RUSSIAN FEDERATION',
	'RW': 'RWANDA',
	'BL': 'SAINT BARTHÉLEMY',
	'SH': 'SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA',
	'KN': 'SAINT KITTS AND NEVIS',
	'LC': 'SAINT LUCIA',
	'MF': 'SAINT MARTIN (FRENCH PART)',
	'PM': 'SAINT PIERRE AND MIQUELON',
	'VC': 'SAINT VINCENT AND THE GRENADINES',
	'WS': 'SAMOA',
	'SM': 'SAN MARINO',
	'ST': 'SAO TOME AND PRINCIPE',
	'SA': 'SAUDI ARABIA',
	'SN': 'SENEGAL',
	'RS': 'SERBIA',
	'SC': 'SEYCHELLES',
	'SL': 'SIERRA LEONE',
	'SG': 'SINGAPORE',
	'SX': 'SINT MAARTEN (DUTCH PART)',
	'SK': 'SLOVAKIA',
	'SI': 'SLOVENIA',
	'SB': 'SOLOMON ISLANDS',
	'SO': 'SOMALIA',
	'ZA': 'SOUTH AFRICA',
	'GS': 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS',
	'SS': 'SOUTH SUDAN',
	'ES': 'SPAIN',
	'LK': 'SRI LANKA',
	'SD': 'SUDAN',
	'SR': 'SURINAME',
	'SJ': 'SVALBARD AND JAN MAYEN',
	'SZ': 'SWAZILAND',
	'SE': 'SWEDEN',
	'CH': 'SWITZERLAND',
	'SY': 'SYRIAN ARAB REPUBLIC',
	'TW': 'TAIWAN, PROVINCE OF CHINA',
	'TJ': 'TAJIKISTAN',
	'TZ': 'TANZANIA, UNITED REPUBLIC OF',
	'TH': 'THAILAND',
	'TL': 'TIMOR-LESTE',
	'TG': 'TOGO',
	'TK': 'TOKELAU',
	'TO': 'TONGA',
	'TT': 'TRINIDAD AND TOBAGO',
	'TN': 'TUNISIA',
	'TR': 'TURKEY',
	'TM': 'TURKMENISTAN',
	'TC': 'TURKS AND CAICOS ISLANDS',
	'TV': 'TUVALU',
	'UG': 'UGANDA',
	'UA': 'UKRAINE',
	'AE': 'UNITED ARAB EMIRATES',
	'GB': 'UNITED KINGDOM',
	'US': 'UNITED STATES',
	'UM': 'UNITED STATES MINOR OUTLYING ISLANDS',
	'UY': 'URUGUAY',
	'UZ': 'UZBEKISTAN',
	'VU': 'VANUATU',
	'VE': 'VENEZUELA, BOLIVARIAN REPUBLIC OF',
	'VN': 'VIET NAM',
	'VG': 'VIRGIN ISLANDS, BRITISH',
	'VI': 'VIRGIN ISLANDS, U.S.',
	'WF': 'WALLIS AND FUTUNA',
	'EH': 'WESTERN SAHARA',
	'YE': 'YEMEN',
	'ZM': 'ZAMBIA',
	'ZW': 'ZIMBABWE',
}

css = """
<style type=\"text/css\">
table {
color: #FAFAFA;
font-family: Helvetica, Arial, sans-serif;
width: 1300px;
border-collapse:
collapse; 
border-spacing: 0;
}

td, th {
border: 1px solid transparent; /* No more visible border */
height: 30px;
}

th {
background: #363636; /* Darken header a bit */
font-weight: bold;
font-size: 25;
}

td {
background: #5a6372;
text-align: center;
font-size: 20;
}

table tr:nth-child(odd) td{
background-color: #5a6372;
}
</style>
"""
# Data collection (opendota & steam)
RAW_MATCH_JSON_DATA_PATH = 'data/match_data_collection/raw_data/'
RAW_MATCH_JSON_DATA_PATH = os.path.join(REPO_PATH, RAW_MATCH_JSON_DATA_PATH)
MATCH_TEMP_PROCESS_LOG = 'data/match_data_collection/temp/temp_process_info.txt' # stores the last  log
MATCH_TEMP_PROCESS_LOG = os.path.join(REPO_PATH, MATCH_TEMP_PROCESS_LOG)
PROCESSED_MATCH_DATA_PATH = 'data/match_data_collection/processed_data'
PROCESSED_MATCH_DATA_PATH = os.path.join(REPO_PATH, PROCESSED_MATCH_DATA_PATH)

# Log stats
NEW_USER_SERVER_IMAGE_PATH = os.path.join(TEMP_IMAGE_PATH, 'new_user_server.jpg')
COMMAND_CALLS_IMAGE_PATH = os.path.join(TEMP_IMAGE_PATH, 'command_calls.jpg')
COMMAND_STATS_IMAGE_PATH = os.path.join(TEMP_IMAGE_PATH, 'command_stats.jpg')

WRITE_TEMP_LOG_AFTER_BATCH = 100
WRITE_JSON_AFTER_BATCH = 100
UPDATE_THREHSHOLD_FOR_MATCH_ID = 345600 # 4 Days
LIMIT = 100000
OPENDOTA_URL = 'https://www.opendota.com/api/explorer?sql='
RANK_ID = 7
GET_PUBLIC_MATCH_TIMEOUT = 10000 #sec
ATTRS_WANTED = ['match_id']
SKILL_BRACKET = {'low': {'start_mmr': 2000, 'end_mmr': 3000},
                 'normal': {'start_mmr': 3000, 'end_mmr':4000},
                 'high': {'start_mmr': 4000, 'end_mmr':5000},
                 'very_high': {'start_mmr': 5000, 'end_mmr':15000}}
