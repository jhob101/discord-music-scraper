# This example requires the 'message_content' intent.

import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    server = discord.utils.find(lambda s: s.name == SERVER, client.guilds)
    print(
        f'We have logged in as {client.user}'
        f' on server {server.name} ({server.id})'
    )

    members = '\n - '.join([member.name for member in server.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.embeds:
        await message.channel.send('This is a youtube link')
        # loop through message.embeds
        for embed in message.embeds:
            print(embed.to_dict()['title'])
            #print(embed.to_dict()['description'].split('\n')[0])
            print(embed.to_dict()['url'])

    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('error'):
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(TOKEN)
