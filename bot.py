import discord
import json
from discord.ext import commands
from samp_client.client import SampClient

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', case_insensitive=True, intents=intents)

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
            data = json.load(file)
        
        samp_servers = data.get('samp_servers', [])
        
        temp_list = []
        
        for server in samp_servers:
            ip = server['ip']
            port = server['port']
            info = await get_server_info(ip, port)
            if info:
                temp_list.append({'hostname': info.hostname, 'players': info.players, 'max_players': info.max_players})
        
        sorted_servers = sorted(temp_list, key=lambda x: x['players'], reverse=True)
        
        top_10_servers = sorted_servers[:10]

        embed1 = discord.Embed(title="Embed 1", description="This is the first embed.", color=0xff0000)

        embed2 = discord.Embed(title="Embed 2", description="This is the second embed.", color=0x00ff00)

        await ctx.send(embeds=[embed1, embed2])

    except Exception as e:
        print(e)
        await ctx.send("An error occurred while trying to get server info.")

@bot.command()
async def addserver(ctx, server_type: str, ip: str, port: int):
    try:
        with open('servers.json', 'r') as file:
            data = json.load(file)
        
        if server_type.lower() == 'samp':
            servers_key = 'samp_servers'
        elif server_type.lower() == 'mta':
            servers_key = 'mta_servers'
        else:
            await ctx.send("Invalid server type. Please use 'samp' or 'mta'.")
            return

        servers = data.get(servers_key, [])

        for server in servers:
            if server['ip'] == ip and server['port'] == port:
                await ctx.send("Server already exists.")
                return

        new_server = {'ip': ip, 'port': port}
        servers.append(new_server)
        data[servers_key] = servers

        with open('servers.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send("Server added successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred while trying to add server: {e}")

@bot.command()
async def players(ctx, address: str, port: int):
    try:
        with SampClient(address=address, port=port) as client:
            info = client.get_server_info()
            players = [client.name for client in client.get_server_clients_detailed()]
            server_name = info.hostname
            players_list = "\n".join(players)
            await ctx.send(f'```Server Name: {info.hostname}\nPlayers: {info.players}/{info.max_players}```\n{players_list}')
    except Exception as e:
        await ctx.send(f"An error occurred while trying to get players info: {e}")

with open("./config.json", 'r') as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["DISCORD_TOKEN"]

@bot.event
async def on_ready():
    activity = discord.Game(name="Orbx Hosting#7091", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is Online!")

bot.run(TOKEN)
