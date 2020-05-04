import os
import random
import discord
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
#all of the tokens are stored in a .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AUTH_TOKEN = os.getenv('BLIZZ_TOKEN')

client = discord.Client()
#client event shows in console that bot is connected
@client.event
async def on_ready():

    print(f'{client.user} has connected to Discord!')
#this event sends a message to a new member in the discord server
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to the server!')

bot = commands.Bot(command_prefix='!')
#basic bot command for rolling a dice
@bot.command(name='roll_dice', help='Rolls dice, input 2 numbers, amount and sides')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))
#this command shows the current title of a character
@bot.command(name='title', help='Current title, type realm & character name')
async def title(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/titles?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    data = requests.get(url)
    data_string = json.loads(data.text)
    print(data_string["active_title"]["name"])
    #shows the title and capitalizes the first letter, because the input has to be in lowercase
    await ctx.send("```" + characterName.capitalize() + " " + data_string["active_title"]["name"]+ "```")

#this command shows every title of a character
@bot.command(name='titles', help="Shows every title of a character, type realm & character name")
async def titles(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/titles?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    r = requests.get(url)
    data = json.loads(r.text)
    type(data["titles"])
    #for loop goes through every title in the json and prints them out
    for title in data["titles"]:
        print(title["name"])
        await ctx.send("```" + characterName.capitalize() + " " + title["name"]+ "```")

#this command shows all the basic info of a character
@bot.command(name='character', help='Shows basic character info, type realm & character name')
async def character(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    data = requests.get(url)
    data_string = json.loads(data.text)
    #this api request is simple, so there is no need for a for loop to go through the list
    await ctx.send("```Character name: " + data_string["name"] + "\n" +
    "Class: " + data_string["character_class"]["name"]+ "\n" +
    "Class specialization: " + data_string["active_spec"]["name"]+ "\n" +
    "Character race: " + data_string["race"]["name"]+ "\n" +
    "Gender: " + data_string["gender"]["name"]+ "\n" +
    "Guild: " + data_string["guild"]["name"] + "\n" +
    "Faction: " + data_string["faction"]["name"]+ "```")
    
  
    
#this command shows characters current gear and basic information of the items
@bot.command(name='armory', help='Shows characters current gear, type realm & character name')
async def armory(ctx, realmSlug: str, characterName: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/equipment?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    
    r = requests.get(url)
    data = json.loads(r.text)
    type(data["equipped_items"])
    #for loop to go through all the equipped items
    for item in data["equipped_items"]:
        await ctx.send("```Item name: "+ item["name"] + "\nItem slot: " + item["slot"]["name"] + "\n" + item["level"]["display_string"] + "```")

#this command shows single item with all the important information     
@bot.command(name='armour', help='Shows single item, type realm, character name & item type(capital letter)')
async def armourpiece(ctx, realmSlug: str, characterName: str, piece: str):
    url = "https://eu.api.blizzard.com/profile/wow/character/%s/%s/equipment?namespace=profile-eu&locale=en_GB&access_token=%s" % (
        realmSlug, characterName, AUTH_TOKEN
    )
    r = requests.get(url)
    data = json.loads(r.text)
    type(data["equipped_items"])
    #for loop to go through the equipped items
    for item in data["equipped_items"]:
        # %s is the input for the item you want to see
        if item["slot"]["name"] == "%s" % (piece):
            #this if tells the bot to go through this list if the typed item is "Head", "Chest" or "Shoulders"
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
             #else it prints out items that do not include azerite_details   
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
