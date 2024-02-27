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
        
        # Create a temporary list to store server info
        temp_list = []
        
        for server in server_list:
            ip = server['ip']
            port = server['port']
            info = await get_server_info(ip, port)
            if info:
                temp_list.append({'hostname': info.hostname, 'players': info.players, 'max_players': info.max_players})
        
        # Sort the servers based on the number of players
        sorted_servers = sorted(temp_list, key=lambda x: x['players'], reverse=True)
        
        # Get the top 10 servers
        top_10_servers = sorted_servers[:10]
        
        # Create an embed
        embed = discord.Embed(title="Top 10 Servers by Players", color=0x00ff00)
        
        # Add server info to the embed
        for idx, server in enumerate(top_10_servers, start=1):
            embed.add_field(name=f"Server {idx}", value=f"**Name:** {server['hostname']}\n**Players:** {server['players']}/{server['max_players']}", inline=False)
        
        # Send the embed
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while trying to get server info.")

@bot.command()
async def addserver(ctx, ip: str, port: int):
    try:
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
async def players(ctx, ADD, NUM):
    try:
        with SampClient(address=ADD, port=NUM) as client:
            info = client.get_server_info()
            players = [client.name for client in client.get_server_clients_detailed()]
            server_name = info.hostname
            players_list = "\n".join(players)
            await ctx.send(f'```Server Name: {info.hostname}\nPlayers: {info.players}/{info.max_players}```')
    except Exception as e:
        await ctx.send(f"An error occurred while trying to get players info: {e}")

# Rest of your code...

bot.run("MTE5MzIyNDUxMTMxOTk2NTg0Ng.GhFz4H.EN9hVxRBNqNuZne3qbUsYoLSsx30tNOMVRAYMQ")
