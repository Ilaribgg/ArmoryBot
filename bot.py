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
AUTH_TOKEN = os.getenv('BLIZZ_TOKEN')

client = discord.Client()

@client.event
async def on_ready():

    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to the server!')

bot = commands.Bot(command_prefix='!')

@bot.command(name='roll_dice', help='Rolls dice, input 2 numbers, amount and sides')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='title', help='Get the current title of a character')
async def title(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/titles?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    data = requests.get(url)
    data_string = json.loads(data.text)
    print(data_string["active_title"]["name"])
    await ctx.send("```" + characterName.capitalize() + " " + data_string["active_title"]["name"]+ "```")

@bot.command(name='titles', help="Shows every title of a character")
async def titles(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/titles?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    r = requests.get(url)
    data = json.loads(r.text)
    type(data["titles"])
    for title in data["titles"]:
        print(title["name"])
        await ctx.send("```" + characterName.capitalize() + " " + title["name"]+ "```")

@bot.command(name='character', help='Shows basic character info')
async def character(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/appearance?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    data = requests.get(url)
    data_string = json.loads(data.text)
    await ctx.send("```Character name: " + data_string["character"]["name"] + "```")
    await ctx.send("```Class: " + data_string["playable_class"]["name"]+ "```")
    await ctx.send("```Class specialization: " + data_string["active_spec"]["name"]+ "```")
    await ctx.send("```Character race: " + data_string["playable_race"]["name"]+ "```")
    await ctx.send("```Gender: " + data_string["gender"]["name"]+ "```")
    await ctx.send("```Faction: " + data_string["faction"]["name"]+ "```")
    

@bot.command(name='armory', help='Shows characters current gear with item level')
async def armory(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/equipment?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    r = requests.get(url)
    data = json.loads(r.text)
    type(data["equipped_items"])
    for item in data["equipped_items"]:
        await ctx.send("```Item name: "+ item["name"] + "\nItem slot: " + item["slot"]["name"] + "\n" + item["level"]["display_string"] + "```")
        
@bot.command(name='head', help='Shows info of head slot item')
async def head(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/equipment?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    r = requests.get(url)
    data = json.loads(r.text)
    type(data["equipped_items"])
    for item in data["equipped_items"]:
        await ctx.send("```Item name: "+ item["name"] + "\nItem slot: " + item["slot"]["type"]["HEAD"] +"```")
    

bot.run(TOKEN)
