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

@bot.command(name='title', help='Current title, type realm & character name')
async def title(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/titles?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    data = requests.get(url)
    data_string = json.loads(data.text)
    print(data_string["active_title"]["name"])
    await ctx.send("```" + characterName.capitalize() + " " + data_string["active_title"]["name"]+ "```")

@bot.command(name='titles', help="Shows every title of a character, type realm & character name")
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

@bot.command(name='character', help='Shows basic character info, type realm & character name')
async def character(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    data = requests.get(url)
    data_string = json.loads(data.text)
    await ctx.send("```Character name: " + data_string["name"] + "\n" +
    "Class: " + data_string["character_class"]["name"]+ "\n" +
    "Class specialization: " + data_string["active_spec"]["name"]+ "\n" +
    "Character race: " + data_string["race"]["name"]+ "\n" +
    "Gender: " + data_string["gender"]["name"]+ "\n" +
    "Guild: " + data_string["guild"]["name"] + "\n" +
    "Faction: " + data_string["faction"]["name"]+ "```")
    
  
    

@bot.command(name='armory', help='Shows characters current gear, type realm & character name')
async def armory(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/equipment?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    r = requests.get(url)
    data = json.loads(r.text)
    type(data["equipped_items"])
    for item in data["equipped_items"]:
        await ctx.send("```Item name: "+ item["name"] + "\nItem slot: " + item["slot"]["name"] + "\n" + item["level"]["display_string"] + "```")
        
@bot.command(name='armour', help='Shows single item, type realm, character name & item type(capital letter)')
async def armourpiece(ctx, realmSlug: str, characterName: str, piece: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/equipment?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    r = requests.get(url)
    data = json.loads(r.text)
    type(data["equipped_items"])
    for item in data["equipped_items"]:
        if item["slot"]["name"] == "%s" % (piece):
            print(item["slot"]["name"])
            if item["slot"]["name"] == "Head" or item["slot"]["name"]== "Chest" or item["slot"]["name"] == "Shoulders":
                await ctx.send("```Item slot: " + item["slot"]["name"] +"\nItem name: "+ item["name"] +  "\n" + item["level"]["display_string"] + "\n" + "\n" +
                "Main stats: " + "\n" + "\n" +
                item["stats"][0]["display"]["display_string"] + "\n" +
                item["stats"][1]["display"]["display_string"] + "\n" + 
                item["stats"][2]["display"]["display_string"] + "\n" + "\n" +
                item["azerite_details"]["selected_powers"][0]["spell_tooltip"]["spell"]["name"] + "\n" +
                item["azerite_details"]["selected_powers"][0]["spell_tooltip"]["description"] + "\n" + "\n" +
                item["azerite_details"]["selected_powers"][1]["spell_tooltip"]["spell"]["name"] + "\n" +
                item["azerite_details"]["selected_powers"][1]["spell_tooltip"]["description"] + "\n" + "\n" +
                item["azerite_details"]["selected_powers"][2]["spell_tooltip"]["spell"]["name"] + "\n" +
                item["azerite_details"]["selected_powers"][2]["spell_tooltip"]["description"] + "\n" + "\n" +
                item["azerite_details"]["selected_powers"][3]["spell_tooltip"]["spell"]["name"] + "\n" +
                item["azerite_details"]["selected_powers"][3]["spell_tooltip"]["description"] + "```")
            else:              
                await ctx.send("```Item slot: " + item["slot"]["name"] +"\nItem name: "+ item["name"] +  "\n" + item["level"]["display_string"] + "\n" + "\n" +
                "Main stats: " + "\n" + "\n" +
                item["stats"][0]["display"]["display_string"] + "\n" +
                item["stats"][1]["display"]["display_string"] + "\n" + 
                item["stats"][2]["display"]["display_string"] + "\n" + "\n" +
                "Secondary stats: " + "\n" + "\n" +
                item["stats"][3]["display"]["display_string"] + "\n" + 
                item["stats"][4]["display"]["display_string"] +  "```")
 
bot.run(TOKEN)
