import discord
import json
import requests
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='bd ',intents=intents)
channel = 1113401488971137024
token = "MTExMzM5OTQ1MjE0MTYzMzYwNg.GK3N0R.f8DWC3OnhA76YooQthenWxByyIfm_Dxtz5OChs"
server = 1045021087060205679

def test(url):
    print("hooks")

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

def send_webhook(url,content,embeds):
    print("hooks")

    message = content
    new_embeds = []
    for embed in embeds :
        new_embeds.append(embed.to_dict())
    data = {
        "content": message ,
        "embeds": new_embeds,
        "attachments": []
        }
    try:
        response = requests.post(url, json=data)
    except:
        return(False)
    
    print(response.status_code)
    if response.status_code != 204:
        raise ValueError(f'Failed to send Discord webhook: {response.text}')

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return
    if message.channel.id == channel:
        with open('data.json','r') as f:
            data = json.load(f)
        webhooks = data['webhooks']
        for hook in webhooks:
            print(message.embeds)
            send_webhook(hook,message.content,message.embeds)

    await client.process_commands(message)

@client.slash_command(name = "subscribe", description = "Sub to notifs", guild=discord.Object(id=server)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(ctx,url):
    if test(url):
        with open('data.json','r') as f:
            data = json.load(f)
        data['webhooks'][ctx.author.id] = url
        with open('data.json','w') as f:
            json.dump(data,f)
        await ctx.respond("Channel added successfully ")
    else:
        await ctx.respond("Invalid url")

@client.slash_command(name = "unsubscribe", description = "Sub to notifs", guild=discord.Object(id=server)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(ctx):
    with open('data.json','r') as f:
        data = json.load(f)
    print(data['webhooks'],ctx.author.id)
    if str(ctx.author.id) in data['webhooks']:
        del data['webhooks'][str(ctx.author.id)]
        with open('data.json','w') as f:
            json.dump(data,f)
        await ctx.respond("Unsubscribed from notification")
    else:
        await ctx.respond("No embeds for this account")




client.run(token) 