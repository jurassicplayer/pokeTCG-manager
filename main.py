#!/usr/bin/python3
import urllib.request
from bs4 import BeautifulSoup
import sqlite3

series='sm-series'
expansion='sm4'
card_num='1'
poke_url='https://www.pokemon.com/us/pokemon-tcg/pokemon-cards'

#Dual color Azumarill
series='ex-series'
expansion='ex11'
#card_num='19'

#Weakness modifier +20 dmg Kakuna
#series='diamond-pearl-series'
#expansion='dp4'
#card_num='73'

#Ability Alolan Raichu
series='sm-series'
expansion='sm4'
card_num='31'

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
    print(card_illustrator)
