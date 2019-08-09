##### General
browser_headers = {'user-agent': 'Mozilla/5.0'}
browser_headers_chrome = {'user-agent': 'Chrome/75.0.3770.80-1'}

##### character_icons Info constant
heroes_pre_url = 'https://www.dotabuff.com/heroes/'
heroes_names = ['abaddon', 'alchemist', 'ancient-apparition', 'anti-mage', 'arc-warden', 'axe', 'bane', 'batrider',
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
                'shadow-shaman', 'silencer', 'skywrath-mage', 'slardar', 'slark', 'sniper', 'spectre', 'spirit-breaker',
                'storm-spirit', 'sven', 'techies', 'templar-assassin', 'terrorblade', 'tidehunter', 'timbersaw',
                'tinker', 'tiny', 'treant-protector', 'troll-warlord', 'tusk', 'underlord', 'undying', 'ursa',
                'vengeful-spirit', 'venomancer', 'viper', 'visage', 'warlock', 'weaver', 'windranger',
                'winter-wyvern', 'witch-doctor', 'wraith-king', 'zeus']


heroes_name_alternative = {'abba': 'abaddon', 'alche':'alchemist', 'aa': 'ancient-apparition', 'am':'anti-mage',
                           'arc' :'arc-warden', 'bat': 'batrider', 'bm': 'beastmaster', 'bs':'bloodseeker',
                           'bh':'bounty-hunter', 'panda': 'brewmaster', 'bb': 'bristleback', 'brood': 'broodmother',
                           'centaur': 'centaur-warrunner', 'ck': 'chaos-knight', 'clock': 'clockwerk',
                           'cm': 'crystal-maiden', 'seer':'dark-seer', 'ds':'dark-seer', 'willow': 'dark-willow',
                           'dp': 'death-prophet', 'thrall': 'disruptor', 'dk': 'dragon-knight', 'drow': 'drow-ranger',
                           'es': 'earthshaker', 'et': 'elder-titan', 'ench': 'enchantress', 'enchan': 'enchantress',
                           'fv': 'faceless-void', 'grim': 'grimstroke','gs': 'grimstroke', 'gyro':'gyrocopter', 'kael': 'invoker',
                           'wisp': 'io', 'jk': 'jakiro', 'jugg': 'juggernaut', 'kotl':'keeper-of-the-light',
                           'lc': 'legion-commander', 'lesh': 'leshrac', 'ls': 'lifestealer', 'naix': 'lifestealer',
                           'ld': 'lone-druid', 'wolf': 'lycan', 'mag': 'magnus', 'potm': 'mirana', 'mk': 'monkey-king',
                           'morp': 'morphling', 'morph': 'morphling', 'naga': 'naga-siren', 'siren': 'naga-siren',
                           'np': 'natures-prophet', 'furion': 'natures-prophet', 'necro': 'necrophos',
                           'ns': 'night-stalker', 'balanar': 'night-stalker', 'nyx': 'nyx-assassin', 'ogre': 'ogre-magi',
                           'omni': 'omniknight', 'od': 'outworld-devourer', 'pango': 'pangolier', 'pa':'phantom-assassin',
                           'pl': 'phantom-lancer', 'qop': 'queen-of-pain', 'sk': 'sand-king', 'sd': 'shadow-demon',
                           'sf': 'shadow-fiend', 'ss': 'shadow-shaman', 'silence': 'silencer', 'sky': 'skywrath-mage',
                           'sb': 'spirit-breaker', 'breaker': 'spirit-breaker', 'barathrum': 'spirit-breaker',
                           'storm': 'storm-spirit', 'techie': 'techies', 'ta': 'templar-assassin',
                           'templar': 'templar-assassin', 'tb': 'terrorblade', 'terror': 'terrorblade',
                           'tide':'tidehunter', 'timber': 'timbersaw', 'tp': 'treant-protector',
                           'treant': 'treant-protector', 'troll': 'troll-warlord', 'vs': 'vengeful-spirit',
                           'veno': 'venomancer', 'wr': 'windranger', 'winter': 'winter-wyvern', 'ww': 'winter-wyvern',
                           'wd': 'witch-doctor', 'wk': 'wraith-king', 'admiral': 'kunkka', 'venge': 'vengeful-spirit',
                           'rhasta': 'shadow-shaman', 'bara': 'spirit-breaker', 'bounty': 'bounty-hunter',
                           'bristle': 'bristleback', 'void': 'faceless-void', 'legion': 'legion-commander',
                           'monkey': 'monkey-king', 'antimage': 'anti-mage', 'apparition': 'ancient-apparition',
                           'ancient': 'ancient-apparition', 'beast':'beastmaster', 'blood': 'bloodseeker',
                           'brew': 'brewmaster', 'chaos': 'chaos-knight', 'ember': 'ember-spirit',
                           'queen': 'queen-of-pain', 'sandking': 'sand-king', 'shadowfiend': 'shadow-fiend',
                           'skywrath': 'skywrath-mage', 'trollwarlord': 'troll-warlord', 'tw': 'troll-warlord',
                           'lanaya': 'templar-assassin', 'nagasiren': 'naga-siren', 'faceless': 'faceless-void',
                           'wyvern': 'winter-wyvern', 'alch': 'alchemist', 'tuskar': 'tusk', 'jug': 'juggernaut',
                           'vengeful': 'vengeful-spirit', 'wraithking': 'wraith-king', 'skywrathmage': 'skywrath-mage',
                           'tider-hunter': 'tidehunter', 'jugger': 'juggernaut', 'sm': 'skywrath-mage',
                           'enchant': 'enchantress', 'darkseer': 'dark-seer', 'windrunner': 'windranger',
                           'spec': 'spectre', 'wraith': 'wraith-king', 'shaman': 'shadow-shaman', 'alc': 'alchemist',
                           'warden': 'arc-warden', 'cent': 'centaur-warrunner', 'clinks': 'clinkz', 'clink': 'clinkz',
                           'invo': 'invoker', 'titan': 'elder-titan', 'night': 'night-stalker',
                           'nature': 'natures-prophet', 'natures':'natures-prophet', 'prophet': 'natures-prophet',
                           'sladar': 'slardar', 'maiden': 'crystal-maiden', 'invoke': 'invoker',
                           'kaldr': 'ancient-apparition', 'magina': 'anti-mage', 'khan': 'axe', 'antropos': 'bane',
                           'jinzakk': 'batrider', 'rexxar': 'beastmaster', 'strygwyr': 'bloodseeker',
                           'gondar': 'bounty-hunter', 'nessaj': 'chaos-knight', 'holy knight': 'chen', 'bone': 'clinkz',
                           'cw': 'clockwerk', 'rylai': 'crystal-maiden', 'ishkafel': 'dark-seer', 'priest': 'dazzle',
                           'shadow priest': 'dazzle', 'krob': 'death-prophet', 'krobelus': 'death-prophet',
                           'lucifer': 'doom', 'luci': 'doom', 'doom bringer': 'doom', 'davion': 'dragon-knight',
                           'traxis': 'drow-ranger', 'shaker': 'earthshaker', 'chantress': 'enchantress',
                           'darchrow': 'enigma', 'darkterror': 'faceless-void', 'aurel': 'gyrocopter',
                           'scared warrior': 'huskar', 'voker': 'invoker', 'jak': 'jakiro', 'yunero': 'juggernaut',
                           'keeper': 'keeper-of-the-light', 'ezalor': 'keeper-of-the-light', 'tormented soul': 'leshrac',
                           'kelthuzad': 'lich', 'slayer': 'lina', 'demon witch': 'lion', 'bear': 'lone-druid',
                           'druid': 'lone-druid', 'syllabear': 'lone-druid', 'moon': 'luna rider', 'lycanthrope': 'lycan',
                           'magnataur': 'magnus', 'dusa': 'medusa', 'gorgon': 'medusa', 'geo': 'meepo', 'geomancer': 'meepo',
                           'slithice': 'naga-siren', 'necrolyte': 'necrophos', 'nerub': 'nyx-assassin',
                           'mortred': 'phantom-assasin', 'azwraith': 'phantom-lancer', 'faerie': 'puck', 'butcher': 'pudge',
                           'oblivion': 'pugna', 'akasha': 'queen-of-pain', 'lightning': 'razor', 'stealth-assasin': 'riki',
                           'magus': 'rubick', 'crix': 'sand-king', 'crixalis': 'sand-king', 'eredar': 'shadow-demon',
                           'nevermore': 'shadow-fiend', 'nortrom': 'silencer', 'leoric': 'wraith-king', 'skeleton king':'wraith-king',
                           'slar': 'slardar', 'murloc': 'slark', 'mercurial': 'spectre', 'kardel': 'sniper',
                           'raijin': 'storm', 'rogue knight': 'sven', 'leviathan': 'tidehunter', 'rizzrak': 'timbersaw',
                           'tink': 'tinker', 'stone giant': 'tiny', 'rooftrellen': 'treant-protector', 'dirge': 'undying',
                           'ulfsaar': 'ursa', 'netherdrake': 'viper', 'necrolic': 'visage', 'alleria': 'windranger',
                           'wind': 'windranger'}


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
icons_path_small = 'data/character_icons/'
icons_path_big   = 'data/character_icons_big/'
icon_x           = -0.1
icon_y           = 0.75
icon_width       = 0.2
icon_height      = 0.05
icon_height_diff = 0.07


# Item
ITEM_NAMES = ['abyssal-blade', 'aegis-of-the-immortal', 'aeon-disk', 'aether-lens', 'aghanims-blessing',
              'aghanims-scepter', 'animal-courier', 'arcane-boots', 'armlet-of-mordiggian',
              'armlet-of-mordiggian-active', 'assault-cuirass', 'band-of-elvenskin', 'battle-fury', 'belt-of-strength',
              'black-king-bar', 'blade-mail', 'blade-mail-axe-pw', 'blade-of-alacrity', 'blades-of-attack',
              'blight-stone', 'blink-dagger', 'bloodstone', 'bloodthorn', 'boots-of-speed', 'boots-of-travel',
              'boots-of-travel-upgrade', 'bottle', 'bottle-arcane', 'bottle-bounty', 'bottle-doubledamage',
              'bottle-empty', 'bottle-haste', 'bottle-illusion', 'bottle-invisibility', 'bottle-medium',
              'bottle-regeneration', 'bottle-small', 'bracer', 'broadsword', 'buckler', 'butterfly', 'chainmail',
              'cheese', 'circlet', 'clarity', 'claymore', 'cloak', 'courier', 'courier-dire', 'courier-dire-flying',
              'courier-radiant-flying', 'crimson-guard', 'crimson-robe', 'crown', 'crystalys', 'daedalus', 'dagon',
              'dagon-level-2', 'dagon-level-3', 'dagon-level-4', 'dagon-level-5', 'default', 'demon-edge', 'desolator',
              'diffusal-blade', 'diffusal-blade-2', 'divine-rapier', 'dragon-lance', 'drum-of-endurance',
              'dust-of-appearance', 'eaglesong', 'echo-sabre', 'emptyitembg', 'enchanted-mango', 'energy-booster',
              'ethereal-blade', 'euls-scepter-of-divinity', 'eye-of-skadi', 'faerie-fire', 'firecrackers',
              'firework-mine', 'flying-courier', 'force-staff', 'gauntlets-of-strength', 'gem-of-true-sight',
              'ghost-scepter', 'glimmer-cape', 'gloves-of-haste', 'greater-clarity', 'greater-salve',
              'greevil-whistle', 'greevil-whistle-toggle', 'guardian-greaves', 'halloween-candy-corn',
              'halloween-rapier', 'hand-of-midas', 'headdress', 'healing-salve', 'heart-of-tarrasque',
              'heavens-halberd', 'helm-of-iron-will', 'helm-of-the-dominator', 'holy-locket', 'hood-of-defiance',
              'hurricane-pike', 'hyperstone', 'infused-raindrops', 'iron-branches', 'iron-talon', 'javelin', 'kaya',
              'kaya-and-sange', 'linkens-sphere', 'lotus-orb', 'maelstrom', 'magic-stick', 'magic-wand', 'manta-style',
              'mantle-of-intelligence', 'mask-of-madness', 'medallion-of-courage', 'mekansm', 'meteor-hammer',
              'mithril-hammer', 'mjollnir', 'monkey-king-bar', 'moon-shard', 'morbid-mask', 'mystery-arrow',
              'mystery-hook', 'mystery-missile', 'mystery-toss', 'mystery-vacuum', 'mystic-staff', 'necronomicon',
              'necronomicon-level-2', 'necronomicon-level-3', 'neutral', 'nian-flag-trap', 'null-talisman',
              'nullifier', 'oblivion-staff', 'observer-and-sentry-wards', 'observer-ward', 'octarine-core', 'ogre-axe',
              'orb-of-venom', 'orchid-malevolence', 'perseverance', 'phase-boots', 'pipe-of-insight', 'place-building',
              'platemail', 'point-booster', 'poor-mans-shield', 'power-treads', 'power-treads-agi', 'power-treads-int',
              'power-treads-str', 'present', 'quarterstaff', 'quelling-blade', 'radiance', 'radiance-inactive',
              'reaver', 'recipe', 'recipe-scroll', 'refresher-orb', 'refresher-shard', 'ring-of-aquila',
              'ring-of-aquila-active', 'ring-of-basilius', 'ring-of-basilius-active', 'ring-of-health',
              'ring-of-protection', 'ring-of-regen', 'ring-of-tarrasque', 'river-painter', 'river-painter2',
              'river-painter3', 'river-painter4', 'river-painter5', 'river-painter6', 'river-painter7',
              'robe-of-the-magi', 'rod-of-atos', 'sacred-relic', 'sages-mask', 'salve', 'sange', 'sange-and-yasha',
              'satanic', 'scythe-of-vyse', 'sentry-ward', 'shadow-amulet', 'shadow-blade', 'shivas-guard',
              'silver-edge', 'skull-basher', 'slippers-of-agility', 'slippers-of-halcyon', 'smoke-of-deceit',
              'solar-crest', 'soul-booster', 'soul-ring', 'spirit-vessel', 'staff-of-wizardry', 'stout-shield',
              'talisman-of-evasion', 'tango', 'tango-shared', 'tombstone', 'tome-of-knowledge', 'town-portal-scroll',
              'traditional-crackers', 'tranquil-boots', 'tranquil-boots-active', 'travel-boots-tinker',
              'travel-slippers', 'ultimate-orb', 'urn-of-shadows', 'vanguard', 'veil-of-discord', 'vitality-booster',
              'vladmir', 'vladmirs-offering', 'void-stone', 'ward-dispenser-sentry', 'wind-lace', 'winter-cake', 'winter-coal',
              'winter-coco', 'winter-cookie', 'winter-greevil-chewy', 'winter-greevil-garbage', 'winter-greevil-treat',
              'winter-ham', 'winter-kringle', 'winter-mushroom', 'winter-skates', 'winter-snowball', 'winter-stocking',
              'winter-woolies', 'wraith-band', 'yasha', 'yasha-and-kaya']


# Dota 2 pro tracker constants
d2pt_hero_names = {'abaddon': 'Abaddon', 'alchemist': 'Alchemist', 'ancient-apparition': 'Ancient Apparition',
                   'anti-mage': 'Anti-Mage', 'arc-warden': 'Arc Warden', 'axe': 'Axe', 'bane': 'Bane',
                   'batrider': 'Batrider', 'beastmaster': 'Beastmaster', 'bloodseeker': 'Bloodseeker',
                   'bounty-hunter': 'Bounty Hunter', 'brewmaster': 'Brewmaster', 'bristleback': 'Bristleback',
                   'broodmother': 'Broodmother', 'centaur-warrunner': 'Centaur Warrunner',
                   'chaos-knight': 'Chaos Knight', 'chen': 'Chen', 'clinkz': 'Clinkz', 'clockwerk': 'Clockwerk',
                   'crystal-maiden': 'Crystal Maiden', 'dark-seer': 'Dark Seer', 'dark-willow': 'Dark Willow',
                   'dazzle': 'Dazzle', 'death-prophet': 'Death Prophet', 'disruptor': 'Disruptor', 'doom': 'Doom',
                   'dragon-knight': 'Dragon Knight', 'drow-ranger': 'Drow Ranger', 'earth-spirit': 'Earth Spirit',
                   'earthshaker': 'Earthshaker', 'elder-titan': 'Elder Titan', 'ember-spirit': 'Ember Spirit',
                   'enchantress': 'Enchantress', 'enigma': 'Enigma', 'faceless-void': 'Faceless Void',
                   'grimstroke': 'Grimstroke', 'gyrocopter': 'Gyrocopter', 'huskar': 'Huskar', 'invoker': 'Invoker',
                   'io': 'Io', 'jakiro': 'Jakiro', 'juggernaut': 'Juggernaut',
                   'keeper-of-the-light': 'Keeper Of The Light', 'kunkka': 'Kunkka',
                   'legion-commander': 'Legion Commander', 'leshrac': 'Leshrac', 'lich': 'Lich',
                   'lifestealer': 'Lifestealer', 'lina': 'Lina', 'lion': 'Lion', 'lone-druid': 'Lone Druid',
                   'luna': 'Luna', 'lycan': 'Lycan', 'magnus': 'Magnus', 'mars': 'Mars', 'medusa': 'Medusa',
                   'meepo': 'Meepo', 'mirana': 'Mirana', 'monkey-king': 'Monkey King', 'morphling': 'Morphling',
                   'naga-siren': 'Naga Siren', 'natures-prophet': 'Natures Prophet', 'necrophos': 'Necrophos',
                   'night-stalker': 'Night Stalker', 'nyx-assassin': 'Nyx Assassin', 'ogre-magi': 'Ogre Magi',
                   'omniknight': 'Omniknight', 'oracle': 'Oracle', 'outworld-devourer': 'Outworld Devourer',
                   'pangolier': 'Pangolier', 'phantom-assassin': 'Phantom Assassin', 'phantom-lancer': 'Phantom Lancer',
                   'phoenix': 'Phoenix', 'puck': 'Puck', 'pudge': 'Pudge', 'pugna': 'Pugna',
                   'queen-of-pain': 'Queen Of Pain', 'razor': 'Razor', 'riki': 'Riki', 'rubick': 'Rubick',
                   'sand-king': 'Sand King', 'shadow-demon': 'Shadow Demon', 'shadow-fiend': 'Shadow Fiend',
                   'shadow-shaman': 'Shadow Shaman', 'silencer': 'Silencer', 'skywrath-mage': 'Skywrath Mage',
                   'slardar': 'Slardar', 'slark': 'Slark', 'sniper': 'Sniper', 'spectre': 'Spectre',
                   'spirit-breaker': 'Spirit Breaker', 'storm-spirit': 'Storm Spirit', 'sven': 'Sven',
                   'techies': 'Techies', 'templar-assassin': 'Templar Assassin', 'terrorblade': 'Terrorblade',
                   'tidehunter': 'Tidehunter', 'timbersaw': 'Timbersaw', 'tinker': 'Tinker', 'tiny': 'Tiny',
                   'treant-protector': 'Treant Protector', 'troll-warlord': 'Troll Warlord', 'tusk': 'Tusk',
                   'underlord': 'Underlord', 'undying': 'Undying', 'ursa': 'Ursa', 'vengeful-spirit': 'Vengeful Spirit',
                   'venomancer': 'Venomancer', 'viper': 'Viper', 'visage': 'Visage', 'warlock': 'Warlock',
                   'weaver': 'Weaver', 'windranger': 'Windranger', 'winter-wyvern': 'Winter Wyvern',
                   'witch-doctor': 'Witch Doctor', 'wraith-king': 'Wraith King', 'zeus': 'Zeus'}
