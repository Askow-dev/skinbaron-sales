#!/usr/bin/env python3
import discord
from bs4 import BeautifulSoup
import requests
import re
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
BASENAME = 'https://skinbaron.de/fr/'
wanted_categories = [
        {'name' : 'Couteau', 'link' : BASENAME + 'csgo/Knife?sort=BP', 'plb': 0.3, 'pub': 300},
        {'name' : 'Gants', 'link' : BASENAME + 'csgo/Gloves?sort=BP', 'plb': 0.3, 'pub': 400},
        {'name' : 'AK47', 'link' : BASENAME + 'csgo/Rifle/AK-47?sort=BP', 'plb': 1, 'pub': 75},
        #{'name' : 'USP-S', 'link' : BASENAME + 'csgo/Pistol/USP-S?sort=BP', 'plb': 1, 'pub': 50},
        #{'name' : 'Glock', 'link' : BASENAME + 'csgo/Pistol/Glock-18?sort=BP', 'plb': 1, 'pub': 30},
        {'name' : 'P250', 'link' : BASENAME + 'csgo/Pistol/P250?sort=BP', 'plb': 1, 'pub': 30},
                     ]

async def get_current_best_deal(url, category):
    elem_global = BeautifulSoup(requests.get(url).content, 'html.parser')
    best_item = {
            'type': elem_global.find_all(class_='product-box')[0].find_all(class_='offer-info')[0].find_all('span')[0].string,
            'skin': elem_global.find_all(class_='product-box')[0].find_all(class_='offer-info')[0].find_all('span')[1].string,
            'wear': elem_global.find_all(class_='product-box')[0].find_all(class_='wear-wrapper')[0].find_all('span')[0].text,
            'img': elem_global.find_all(class_='product-box')[0].find_all('img')[0]['src'],
            'price': elem_global.find_all(class_='product-box')[0].find_all(class_='price item')[0].string,
            'reduction': elem_global.find_all(class_='product-box')[0].find_all(class_='pricereduction')[0].string,
            'link': BASENAME + re.findall(r'(offers\/show\?offerUuid=[-&a-f0-9]*)&a;', elem_global.find_all('script', id='skinbaron-frontend-state')[0].string)[0],
            'category': category,
            }
    return best_item

async def send_Item(item, channel):
    embedVar = discord.Embed(title="Meilleur reduction pour la categorie " + item['category']['name'], description="Prix entre " + str(item['category']['lower']) + '€ et ' + str(item['category']['higher']) + '€', color=0x00ff00)
    embedVar.add_field(name=item['type'] + ' | ' + item['skin'], value=item['price'] + " avec une reduction de " + item['reduction'], inline=False)
    embedVar.add_field(name='Etat', value=item['wear'], inline=True)
    embedVar.add_field(name="Lien direct", value='[Lien](' + item['link'] + ')', inline=True)
    embedVar.set_image(url=item['img'])
    await channel.send(embed=embedVar)

@client.event
async def on_ready():
    print(f'{client.user} is connected')
    channel = client.get_channel(int(os.environ.get('DISCORD_CHANNEL')))
    for item in wanted_categories:
        best_item = await best_task[item['name']]
        await send_Item(best_item, channel)
    await client.close()
best_task = {}
for item in wanted_categories:
    URL = item['link'] + '?plb=' + str(item['plb']) + '&pub=' + str(item['pub']) + '&sort=PB'
    best_task[item['name']] = get_current_best_deal(URL, {'name': item['name'], 'higher': item['pub'], 'lower': item['plb']})
client.run(os.environ.get('DISCORD_KEY'))
