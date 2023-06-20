import discord
import json
import requests
from discord.ext import commands
from discord import app_commands


intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='bd ',intents=intents)
channel = 1105900747687731252
token = "MTExNTU4NDIzNDQ1NTg0NjkyMg.GI30A3.GijC80v-TKiGgwYy1Q_k5l85mNjQgRiR7eF5vw"

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
        with open('/data/data.json','r') as f:
            data = json.load(f)
        webhooks = data['webhooks']
        for hook in webhooks:
            print(webhooks[hook])
            send_webhook(webhooks[hook],message.content,message.embeds)

    await client.process_commands(message)

@client.tree.command(name="subscribe") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def subsribe(ctx,url:str):
    if test(url):
        with open('/data/data.json','r') as f:
            data = json.load(f)
        data['webhooks'][str(ctx.user.id)] = url
        with open('/data/data.json','w') as f:
            json.dump(data,f)
        await ctx.response.send_message("Channel added successfully ")
    else:
        await ctx.response.send_message("Invalid url")

@client.tree.command(name="unsubscribe") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def unsubscribe(ctx):
    with open('/data/data.json','r') as f:
        data = json.load(f)
    if str(ctx.user.id) in data['webhooks']:
        del data['webhooks'][str(ctx.user.id)]
        with open('/data/data.json','w') as f:
            json.dump(data,f)
        await ctx.response.send_message("Unsubscribed from notification")
    else:
        await ctx.response.send_message("No embeds for this account")




client.run(token) 