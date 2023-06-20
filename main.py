import discord
import json
import requests
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from pymongo import MongoClient
import os

intents = discord.Intents.default()
intents.message_content = True
load_dotenv()

client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='bd ',intents=intents)
channel = os.getenv("channel")
token = os.getenv("token")
database = os.getenv("database")

cluster = MongoClient(database)
db = cluster['customer-service-bot']
webhooks = db['broadcast']

def test(url):
    message = "This channel has been added as webhook broadcast for torchlabs"
    data = {
        "content": message ,
        "embeds": [],
        "attachments": []
        }
    try:
        response = requests.post(url, json=data)
    except:
        return(False)
    print(response.status_code)
    if response.status_code == 204:
        return(True)
    else:
        return(False)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    try:
        synced = await client.tree.sync()
        print(f'synced{synced}')
    except Exception as e:
        print(e)

def send_webhook(url,content,embeds):
    print("sending hooks")

    message = content
    new_embeds = []
    for embed in embeds :
        new_embeds.append(embed.to_dict())
    data = {
        "content": message ,
        "embeds": new_embeds,
        "attachments": []
        }
    response = requests.post(url, json=data)
    print(response.status_code)

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return
    if message.channel.id == channel:
        hooks = webhooks.find({})
        for user in hooks:
            for hook in user['hooks']:
                send_webhook(user['hooks'][hook],message.content,message.embeds)
    await client.process_commands(message)

@client.tree.command(name="subscribe") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def subsribe(ctx,url:str,nickname:str):
    if test(url):
        user_id = ctx.user.id
        user = webhooks.find_one({"user_id":user_id})
        if user == None:
            user = {"user_id":user_id,"hooks":{}}
            user['hooks'][nickname] = url
            webhooks.insert_one(user)
            await ctx.response.send_message("Channel added successfully")
            return
        else:
            print(len(user['hooks']))
            if len(user['hooks']) < 5:
                webhooks.delete_one({"user_id":user_id})
                user['hooks'][nickname] = url
                webhooks.insert_one(user)
                await ctx.response.send_message("Channel added successfully")
                return
            else:
                await ctx.response.send_message("You have exceeded the limit clear a existing url to add a new one")
                return
    else:
        await ctx.response.send_message("Invalid url")
        return

@client.tree.command(name="unsubscribe") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def unsubscribe(ctx,nickname:str="none"):
    user_id = ctx.user.id
    record = webhooks.find_one({"user_id":user_id})
    if record != None:
        if nickname in record['hooks']:
            del record['hooks'][nickname]
            webhooks.delete_one({"user_id":user_id})
            webhooks.insert_one(record)
        await ctx.response.send_message("Unsubscribed from notification")
    else:
        await ctx.response.send_message("No embeds for this account")
    
@client.tree.command(name="show_subscriptions") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def show(ctx):
    user_id = ctx.user.id
    record = webhooks.find_one({"user_id":user_id})
    if record != None:
        embed=discord.Embed(title="subscriptions", description="list of ur current subscriptions")
        for hook in record['hooks']:
            print(hook)
            embed.add_field(name=hook, value=record['hooks'][hook], inline=False)
        await ctx.response.send_message(embed=embed,ephemeral=True)
        return
    await ctx.response.send_message("No subscriptions yet")




client.run(token) 