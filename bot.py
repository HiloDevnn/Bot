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
        
        # Send the top 10 servers as a message
        if top_10_servers:
            message = "Top 10 Servers by Players:\n"
            for idx, server in enumerate(top_10_servers, start=1):
                message += f"{idx}. {server['hostname']} - {server['players']}/{server['max_players']} players\n"
            await ctx.send(message)
        else:
            await ctx.send("No servers found or all servers unreachable.")
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while trying to get server info.")

# Rest of your code...

bot.run("YOUR_DISCORD_TOKEN")
