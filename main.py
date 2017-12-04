#!/usr/bin/python3
import urllib.request
#from bs4 import BeautifulSoup
import sqlite3
from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype

series='sm-series'
expansion='sm4'
card_num='1'
#poke_url='https://www.pokemon.com/us/pokemon-tcg/pokemon-cards'

#Dual color Azumarill
#series='ex-series'
#expansion='ex11'
#card_num='19'

#Weakness modifier +20 dmg Kakuna
#series='diamond-pearl-series'
#expansion='dp4'
#card_num='73'

#Ability Alolan Raichu
#series='sm-series'
#expansion='sm4'
#card_num='31'



def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file
        :param dbfile: database file
        :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def insert_card(card):
    card_id = card.id                                   #Pokemon card id (Official Pokemon website)
    card_name = card.name                               #Pokemon Name
    card_national_dex = card.national_pokedex_number    #National Pokedex Number
    card_image_SD = card.image_url
    card_image_HD = card.image_url_hi_res
    card_types = card.types                             #Pokemon Type
    card_supertype = card.supertype                     #Pokemon, Trainer, Energy
    card_subtype = card.subtype                         #Stage 1, Stage 2, Item, Supporter, Special Energy
    card_hp = card.hp
    card_number = card.number
    card_illustrator = card.artist
    card_rarity = card.rarity
    card_series = card.series
    card_expansion = card.set
    card_expansion_code = card.set_code
    card_expansion_code_ptcgo = ""  #<FIXME>
    card_text = card.text
    card_ability = card.ability
    card_ancient_trait = card.ancient_trait
    card_attacks = card.attacks
    card_weaknesses = card.weaknesses
    card_resistances = card.resistances
    card_retreat_cost = card.retreat_cost
    card_index = (
        card_id,
        card_name,
        card_expansion_code,
        card_number,
        card_national_dex,
        #card_types,
        card_subtype,
        card_supertype,
        card_illustrator,
        card_image_SD,
        card_image_HD,
        card_rarity,
        card_hp,
        card_text,
        card_weaknesses,
        card_resistances,
        #card_retreat_cost,
        card_ancient_trait,
        card_ability,
        card_ability,
        card_ability
        )
    insert_energy_cost(card_id, 'Pokemon Type', card_types)
    insert_energy_cost(card_id, 'Retreat', card_retreat_cost)
    
    c = conn.cursor()
    print("INSERT INTO Card VALUES {}".format(card_index))
    # c.execute("INSERT INTO Card VALUES {}".format(card_index))

def insert_energy_cost(card_id, energy_cost_type, energy_cost_array, energy_cost_attackID=None):
    print(
        "Inserting energy:\n{}\n{}\n{}\n{}".format(card_id, energy_cost_type, energy_cost_array, energy_cost_attackID)
    )
    energy_cost_converted = 0
    colorless_energy = 0
    darkness_energy = 0
    fairy_energy = 0
    fighting_energy = 0
    fire_energy = 0
    grass_energy = 0
    lightning_energy = 0
    metal_energy = 0
    psychic_energy = 0
    water_energy = 0
    
    if not energy_cost_array:
    
    for energy in energy_cost_array:
        if 'Colorless' in energy:
            colorless_energy    += 1
        if 'Darkness' in energy:
            darkness_energy     += 1
        if 'Fairy' in energy:
            fairy_energy        += 1
        if 'Fighting' in energy:
            fighting_energy     += 1
        if 'Fire' in energy:
            fire_energy         += 1
        if 'Grass' in energy:
            grass_energy        += 1
        if 'Lightning' in energy:
            lightning_energy    += 1
        if 'Metal' in energy:
            metal_energy        += 1
        if 'Psychic' in energy:
            psychic_energy      += 1
        if 'Water' in energy:
            water_energy        += 1
        energy_cost_converted   += 1
    
    energy_index = (
        card_id,
        energy_cost_type,       ## Pokemon Type, Retreat, Attack
        energy_cost_attackID,   ## None, None, Attack Name
        energy_cost_converted,  ## Converted cost (number)
        colorless_energy,
        darkness_energy,
        fairy_energy,
        fighting_energy,
        fire_energy,
        grass_energy,
        lightning_energy,
        metal_energy,
        psychic_energy,
        water_energy
        )

cards = Card.where(set='generations').where(supertype='pokemon').all()
conn = create_connection("ptcg.db")
for card in cards:
    insert_card(card)

'''
database = sqlite3.connect("ptcg.db")
c = database.cursor()
with urllib.request.urlopen('{}/{}/{}/{}'.format(poke_url, series, expansion, card_num)) as response:
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    card_id = soup.find(class_="full-card-information").get('data-card-id')
    card_image = soup.find(class_="card-image").find('img').get('src')
    card_name = soup.find(class_="card-description").find('div').find('h1').text
    card_type = soup.find(class_="card-type").find('h2').text
    try:
        card_preevolution = soup.find(class_="card-type").find('h4').find('a').text.strip()
    except: pass
    if "Trainer" not in card_type:
        card_hp = soup.find(class_="card-hp").text[2:]
        card_poketype = []
        poketypes = soup.find(class_="card-basic-info").find(class_="right").find_all('a')
        for poketype in poketypes:
            card_poketype.append(poketype.find('i').get('class')[1][5:])
        card_pokemon_abilities = soup.find(class_="pokemon-abilities")
        card_pokemon_attacks = card_pokemon_abilities.find_all(class_="ability")
        ##card_ability = soup.find_all(class_="ability").find('div').find('h1').text##
        #card_poke_ability = [ soup.find(class_='poke-ability').text,  soup.find(class_='pokemon-abilities').find('h3').text.split()[len(soup.find(class_='poke-ability').text):], soup.find(class_='pokemon-abilities').find('p').text ]
        #print(soup.find(class_='pokemon-abilities').find('h3').text) #.split())
        card_stats = soup.find_all(class_="stat")
        for stat in card_stats:
            stat_category = stat.find('h4').text
            if stat_category == 'Weakness':
                try:
                    weakness_type = stat.find('ul').find('li').get('title')
                    weakness_modifier = stat.find('ul').find('li').text.split()[0]
                except:
                    print('No weaknesses?')
            if stat_category == 'Resistance':
                try:
                    resistance_type = stat.find('ul').find('li').get('title')
                    resistance_modifier = stat.find('ul').find('li').text.split()[0]
                except:
                    print('No resistances?')
                pass
            if stat_category == 'Retreat Cost':
                try:
                    retreat_costs = stat.find('ul').find_all('li')
                except:
                    retreat_cost = '0'
    card_expansion = soup.find(class_='stats-footer').find('h3').find('a').text
    card_number = soup.find(class_='stats-footer').find('span').text.split()[0].split('/')
    card_expansion_icon = soup.find(class_="expansion").find('a').find('i').get('style')
    card_illustrator = soup.find(class_="illustrator").find('h4').find('a').text
    print(card_pokemon_attacks)
'''
