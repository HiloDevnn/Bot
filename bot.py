import discord
import json
from discord.ext import commands
from samp_client.client import SampClient

bot = commands.Bot(command_prefix='$', case_insensitive=True)

async def get_server_info(address, port):
    try:
        with SampClient(address=address, port=port) as client:
            info = client.get_server_info()
            return info
    except Exception as e:
        print(f"Error getting server info for {address}:{port}: {e}")
        return None

@bot.command()
async def check(ctx):
    try:
        with open('servers.json', 'r') as file:
            server_list = json.load(file)
        
        most_players_server = None
        max_players = -1
        
        for server in server_list:
            ip = server['ip']
            port = server['port']
            info = await get_server_info(ip, port)
            if info and info.players > max_players:
                most_players_server = info
                max_players = info.players
        
        if most_players_server:
            await ctx.send(f"Most players found on {most_players_server.hostname} with {most_players_server.players} players.")
        else:
            await ctx.send("No servers found or all servers unreachable.")
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while trying to get server info.")

@bot.command()
async def add_server(ctx, ip, port):
    try:
        # Your code to add the server goes here
        with open('servers.json', 'r') as file:
            servers = json.load(file)
        
        # Check if the server already exists
        for server in servers:
            if server['ip'] == ip and server['port'] == port:
                await ctx.send("Server already exists.")
                return

        # Add the new server to the list
        new_server = {'ip': ip, 'port': port}
        servers.append(new_server)

        # Save the updated server list back to the file
        with open('servers.json', 'w') as file:
            json.dump(servers, file, indent=4)

        await ctx.send("Server added successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred while trying to add server: {e}")

@bot.command()
async def addserver(ctx, ip: str, port: int):
    await add_server(ctx, ip, port)
    
    
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
