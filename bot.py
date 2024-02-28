import discord
import json
from discord.ext import commands
from samp_client.client import SampClient

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print('Bot is Online!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please use $help for a list of commands.")
    else:
        print(f'Error in command {ctx.command.name}: {error}')

@bot.command(name='check', help='Displays the top 10 SA-MP servers.')
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

        embeds = []

        embed1 = discord.Embed(title="<:orbx:1188474625429082142> Orbx Hosting TOP 10 SA:MP Servers", color=0xf1bc48)
        embed1.set_image(url="https://media.discordapp.net/attachments/1172640694939168808/1188495474525741158/20231224_155630.jpg?ex=659abbaa&is=658846aa&hm=47d25a69bfcc1a676ac6d2f6a323d1a21ba09dcd17318f85edacd8e468cacdae&")

        num_to_emoji = {
            1: '1️⃣',
            2: '2️⃣',
            3: '3️⃣',
            4: '4️⃣',
            5: '5️⃣',
            6: '6️⃣',
            7: '7️⃣',
            8: '8️⃣',
            9: '9️⃣',
            10: '🔟'
        }

        description1 = ""
        for idx, server in enumerate(top_10_servers, start=1):
            emoji = num_to_emoji.get(idx, '⁉️')
            description1 += f"{emoji} ```{server['players']}/{server['max_players']}``` | {server['hostname']}\n"

        embed1.description = description1
        embeds.append(embed1)

        embed2 = discord.Embed(title="", description="4600 Players Are Now Connected To All This Orbx Servers\nNext Refresh In || 0 minutes ||", color=0xf1bc48)
        embed2.set_footer(text="Orbx Status | All rights Reserved 2023 - 2024", icon_url="https://cdn.discordapp.com/attachments/1172640694939168808/1188462447921733703/20231224_132801.jpg?ex=659a9ce8&is=658827e8&hm=3038be5bee65b6d90313e270b416010e8bbc4f4f43439c13d0496cac886fe673&")
        
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)

    except Exception as e:
        print(f'Error in command check: {e}')
        await ctx.send("An error occurred while trying to get server info.")

@bot.command(name='addserver', help='Adds a server to the top 10 list.')
@commands.has_role('Admin')
async def addserver(ctx, server_type: str, ip: str, port: int):
    try:
        with open('servers.json', 'r') as file:
            data = json.load(file)

        servers_key = 'samp_servers' if server_type.lower() == 'samp' else 'mta_servers'
        servers = data.get(servers_key, [])

        # Check if the server already exists
        for server in servers:
            if server['ip'] == ip and server['port'] == port:
                await ctx.send("Server already exists.")
                return

        # Add the new server to the list
        new_server = {'ip': ip, 'port': port}
        servers.append(new_server)
        data[servers_key] = servers

        # Save the updated server list back to the file
        with open('servers.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send("Server added successfully.")

    except Exception as e:
        print(f'Error in command addserver: {e}')
        await ctx.send(f"An error occurred while trying to add server: {e}")

@bot.command(name='players', help='Displays the number of players in a server.')
async def players(ctx, ip: str, port: int):
    try:
        with SampClient(address=ip, port=port) as client:
            info = client.get_server_info()
            players = [client.name for client in client.get_server_clients_detailed()]
            server_name = info.hostname
            players_list = "\n".join(players)
            await ctx.send(f'```Server Name: {info.hostname}\nPlayers: {info.players}/{info.max_players}\nPlayer List:\n{players_list}```')

    except Exception as e:
        await ctx.send(f"An error occurred while trying to get players info: {e}")

if __name__ == '__main__':
    with open("./config.json", 'r') as configjsonFile:
        configData = json.load(configjsonFile)
        TOKEN = configData["DISCORD_TOKEN"]

    bot.run(TOKEN)
