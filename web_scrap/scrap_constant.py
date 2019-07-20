##### General
browser_headers = {'user-agent': 'Mozilla/5.0'}


##### character_icons Info constant
heroes_pre_url = 'https://www.dotabuff.com/heroes/'
heros_names = ['abaddon', 'alchemist', 'ancient-apparition', 'anti-mage', 'arc-warden', 'axe', 'bane', 'batrider',
               'beastmaster', 'bloodseeker', 'bounty-hunter', 'brewmaster', 'bristleback', 'broodmother',
               'centaur-warrunner', 'chaos-knight', 'chen', 'clinkz', 'clockwerk', 'crystal-maiden', 'dark-seer',
               'dark-willow', 'dazzle', 'death-prophet', 'disruptor', 'doom', 'dragon-knight', 'drow-ranger',
               'earth-spirit', 'earthshaker', 'elder-titan', 'ember-spirit', 'enchantress', 'enigma', 'faceless-void',
               'grimstroke', 'gyrocopter', 'huskar', 'invoker', 'io', 'jakiro', 'juggernaut', 'keeper-of-the-light',
               'kunkka', 'legion-commander', 'leshrac', 'lich', 'lifestealer', 'lina', 'lion', 'lone-druid', 'luna',
               'lycan', 'magnus', 'mars', 'medusa', 'meepo', 'mirana', 'monkey-king', 'morphling', 'naga-siren',
               'natures-prophet', 'necrophos', 'night-stalker', 'nyx-assassin', 'ogre-magi', 'omniknight', 'oracle',
               'outworld-devourer', 'pangolier', 'phantom-assassin', 'phantom-lancer', 'phoenix', 'puck', 'pudge',
               'pugna', 'queen-of-pain', 'razor', 'riki', 'rubick', 'sand-king', 'shadow-demon', 'shadow-fiend',
               'shadow-shaman', 'silencer', 'skywrath-mage', 'sladar', 'slark', 'sniper', 'spectre', 'spirit-breaker',
               'storm-spirit', 'sven', 'techies', 'templar-assassin', 'terrorblade', 'tidehunter', 'timbersaw',
               'tinker', 'tiny', 'treant-protector', 'troll-warlord', 'tusk', 'underlord', 'undying', 'ursa',
               'vengeful-spirit', 'venomancer', 'viper', 'visage', 'warlock', 'weaver', 'windranger',
               'winter-wyvern', 'witch-doctor', 'wraith-king', 'zeus']


heroes_section_wanted = ['Worst Versus', 'Best Versus', 'Most Used Items']
section_column_count = {'Worst Versus': 4, 'Best Versus': 4, 'Most Used Items': 3}
section_column_wanted = {'Worst Versus':    ['Hero', 'Disadvantage', 'Win Rate', 'Matches'],
                         'Best Versus':     ['Hero', 'Advantage', 'Win Rate', 'Matches'],
                         'Most Used Items': ['Item', 'Matches', 'Win Rate']}


##### Current trends constant
heroes_trend_url = 'https://www.dotabuff.com/heroes/trends'
heroes_trend_columns = ['Hero', 'WR:Old', 'WR:New', 'WR:Change', 'WR:Trend',
                        'PR:Old', 'PR:New', 'PR:Change', 'PR:Trend']
heros_unwanted_columns = ['WR:Trend', 'PR:Trend']
trend_attribute_key_name = 'data-value'
heroes_trend_image_path = 'web_scrap/data/current_trend/current_trend.png'


##### Matplot icon display settings
icons_path = 'data/character_icons/'
icon_x           = -0.1
icon_y           = 0.75
icon_width       = 0.2
icon_height      = 0.05
icon_height_diff = 0.07

