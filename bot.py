import os
import random
import discord
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():

    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to the server!')
bot = commands.Bot(command_prefix='!')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='title')
async def title(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/titles?namespace=profile-eu&locale=en_GB&access_token=USdNMrSB14iaSYz7GWq4GDtM1p54Cs7Obk" % (
        realmSlug, characterName
    )
    
    data = requests.get(url)
    data_string = json.loads(data.text)
    print(data_string["active_title"]["name"])
    await ctx.send(characterName.capitalize() + " " + data_string["active_title"]["name"])

@bot.command(name='titles')
async def titles(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/titles?namespace=profile-eu&locale=en_GB&access_token=USdNMrSB14iaSYz7GWq4GDtM1p54Cs7Obk" % (
        realmSlug, characterName
    )
    
    data = requests.get(url)
    data_string = json.loads(data.text)
    await ctx.send(data_string["titles"]["title"]["name"])
    
client.run(TOKEN)
bot.run(TOKEN)
