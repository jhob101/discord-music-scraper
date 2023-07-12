import datetime
import os
import discord
from dotenv import load_dotenv
from ytOauth import makePlaylist, addItemToPlaylist, makeService

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def get_playlist_id(service):
    filename = 'months.txt'

    if not os.path.exists(filename):
        file = open("months.txt", "w+")  # create file if it doesn't exist
        print(f'File "{filename}" created.')
    else:
        file = open("months.txt", "r+")
        print(f'File "{filename}" already exists.')

    # get the current month/year as a string
    name = datetime.datetime.now().strftime("%B-%Y")

    # read each line of the file and see if it starts with the current month/year
    for line in file:
        print(line)
        if line.startswith(name):
            # if it does return the playlist id
            print('found a playlist for this month')
            file.close()
            return line.split()[1]

    # if it doesn't exist, create it
    print('creating a new playlist')
    new_id = makePlaylist(service, name)
    #content = file.read()
    #print(f'{content}')
    file.seek(0, 0)  # Move the file pointer to the beginning
    file.write(name + " " + new_id + "\n")
    file.close()
    return new_id


def yt_add_to_playlist(id):
    service = makeService()
    pl_id = get_playlist_id(service)
    addItemToPlaylist(service, pl_id, [id])
    print("added song")
    # return queries
    return pl_id


@client.event
async def on_ready():
    server = discord.utils.find(lambda s: s.name == SERVER, client.guilds)
    print(
        f'We have logged in as {client.user}'
        f' on server {server.name} ({server.id})'
    )

    members = '\n - '.join([member.name for member in server.members])
    print(f'Server Members:\n - {members}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.embeds:
        await message.channel.send('This is a youtube link')
        # loop through message.embeds
        for embed in message.embeds:
            print(embed.to_dict()['title'])
            # print(embed.to_dict()['description'].split('\n')[0])
            print(embed.to_dict()['url'])
            print(embed.to_dict())
            yt_add_to_playlist(embed.to_dict()['url'].split('?v=')[1])

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
