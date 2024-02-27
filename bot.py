import discord
import json
import asyncio
from discord.ext import commands
from samp_client.client import SampClient
import requests

bot = commands.Bot(command_prefix='$', case_insensitive=True)

# Variable to store the token after login
ogp_token = None

async def get_server_info(address, port):
    try:
        with SampClient(address=address, port=port) as client:
            info = client.get_server_info()
            return info
    except Exception as e:
        print(f"Error getting server info for {address}:{port}: {e}")
        return None

async def login_and_get_servers(ctx):
    global ogp_token
    try:
        value1 = "botstatus"
        value2 = "ssbotsshta6483"
        response = requests.post('http://178.62.220.38:56727/ogp_api.php?token/create', data={'user': value1, 'password': value2})
        if response.status_code == 200:
            ogp_token = response.json()['message']
            await ctx.send("Logged in successfully and token obtained.")
            
            # Get list of servers
            server_list_response = requests.post('http://178.62.220.38:56727/ogp_api.php?user_games/list_servers', data={'token': ogp_token})
            server_list = server_list_response.json()['message']
            
            most_players_server = None
            max_players = -1
            
            for server in server_list:
                ip = server['address']
                port = server['port']
                info = await get_server_info(ip, port)
                if info and info.players > max_players:
                    most_players_server = info
                    max_players = info.players
            
            if most_players_server:
                await ctx.send(f"Most players found on {most_players_server.hostname} with {most_players_server.players} players.")
            else:
                await ctx.send("No servers found or all servers unreachable.")
            
        else:
            await ctx.send("Failed to login. Check your username and password.")
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while trying to login.")

@bot.command()
async def login(ctx):
    await login_and_get_servers(ctx)

@bot.command()
async def players(ctx, ADD, NUM):
    with SampClient(address=ADD, port=NUM) as client:
        info = client.get_server_info()
        players = [client.name for client in client.get_server_clients_detailed()]
        server_name = info.hostname
        players_list = "\n".join(players)
        await ctx.send(f'```Server Name: {info.hostname}\nPlayers: {info.players}/{info.max_players}```')

@players.error
async def players_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Usage: $players [ip] [port]')

# Rest of your code...

with open("./config.json", 'r') as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["DISCORD_TOKEN"]

@bot.event
async def on_ready():
    activity = discord.Game(name="Orbx Hosting#7091", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is Online!")

bot.run(TOKEN)
