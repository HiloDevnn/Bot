import discord
import json
from discord.ext import commands, tasks
from samp_client.client import SampClient

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='T$', case_insensitive=True, intents=intents)

# Function to get server info
async def get_server_info(address, port):
    try:
        async with SampClient(address=address, port=port) as client:
            await asyncio.sleep(1)  # Add a 1-second delay
            try:
                info = await client.get_server_info()
            except asyncio.TimeoutError:
                print(f"Timeout error getting server info for {address}:{port}")
                return None
            except Exception as e:
                print(f"Error getting server info for {address}:{port}: {e}")
                return None
            return info
    except Exception as e:
        print(f"Error creating or closing SampClient instance for {address}:{port}: {e}")
        return None
    finally:
        await client.close()

# Command to checktop server info
@bot.command()
async def checktop(ctx):
    try:
        with open('servers.json', 'r') as file:
            data = json.load(file)
        
        samp_servers = data.get('samp_servers', [])
        
        # Create a temporary list to store server info
        samp_temp_list = []
        
        # Get SA:MP servers info
        for server in samp_servers:
            ip = server['ip']
            port = server['port']
            info = await get_server_info(ip, port)
            if info:
                samp_temp_list.append({'hostname': info.hostname, 'players': info.players, 'max_players': info.max_players})
        
        # Calculate total players for SA:MP servers
        total_samp_players = sum(server['players'] for server in samp_temp_list)
        
        # Sort the SA:MP servers based on the number of players
        sorted_samp_servers = sorted(samp_temp_list, key=lambda x: x['players'], reverse=True)
        
        # Get the top 10 servers
        top_10_samp_servers = sorted_samp_servers[:10]
        
        # Create the first embed for SA:MP servers
        embed1_samp = discord.Embed(title="<:orbx:1188474625429082142> Orbx Hosting Top 10 SA:MP Servers", color=0xf1bc48)
        embed1_samp.set_image(url="https://media.discordapp.net/attachments/1172640694939168808/1188495474525741158/20231224_155630.jpg?ex=659abbaa&is=658846aa&hm=47d25a69bfcc1a676ac6d2f6a323d1a21ba09dcd17318f85edacd8e468cacdae&")
        
        # Emoji dictionary
        num_to_emoji = {
            1: '<:o1:1212494930765807697>',
            2: '<:o2:1212495279731773541>',
            3: '<:o3:1212495353195135036>',
            4: '<:o4:1212495407398264852>',
            5: '<:o5:1212495469612236890>',
            6: '<:o6:1212495520937939005>',
            7: '<:o7:1212495558342610955>',
            8: '<:o8:1212495598381437009>',
            9: '<:o9:1212495631390613544>',
            10: '<:o10:1212495663804317726>'
        }
        
        # Add server info to the first embed for SA:MP servers
        description1_samp = ""
        for idx, server in enumerate(top_10_samp_servers, start=1):
            emoji = num_to_emoji.get(idx, '⁉️')
            description1_samp += f"{emoji} ```{server['players']}/{server['max_players']}``` | {server['hostname']}\n"
        
        # Set the description of the first embed for SA:MP servers
        embed1_samp.description = description1_samp
        
        # Create the second embed
        total_players_text = f"<:orbx:1188474625429082142> {total_samp_players} Players Are Now Connected To All These Orbx Servers.\n<a:refresh:1204575037974384751> Next Refresh in: || 10 minutes || ⏱️"
        embed2 = discord.Embed(title="", description=total_players_text, color=0xf1bc48)
        embed2.set_footer(text="Orbx Hosting | All rights Reserved 2023 - 2024", icon_url="https://cdn.discordapp.com/attachments/1172640694939168808/1188462447921733703/20231224_132801.jpg?ex=659a9ce8&is=658827e8&hm=3038be5bee65b6d90313e270b416010e8bbc4f4f43439c13d0496cac886fe673&")
        embed2.set_image(url="https://media.discordapp.net/attachments/1172640694939168808/1188495474525741158/20231224_155630.jpg?ex=659abbaa&is=658846aa&hm=47d25a69bfcc1a676ac6d2f6a323d1a21ba09dcd17318f85edacd8e468cacdae&")
        
        # Fetch and edit the existing message
        guild = bot.get_guild(1150160889996136459)
        channel = guild.get_channel(1211807374885789726)
        
        message = await channel.fetch_message(1212513392976199822)
        
        await message.edit(embeds=[embed1_samp, embed2])
        
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while trying to update the message.")

# Command to add a server
@bot.command()
async def addserver(ctx, server_type: str, ip: str, port: int):
    try:
        with open('servers.json', 'r') as file:
            data = json.load(file)
        
        # Check if the server type exists in the JSON data
        if server_type.lower() == 'samp':
            servers_key = 'samp_servers'
        elif server_type.lower() == 'mta':
            servers_key = 'mta_servers'
        else:
            await ctx.send("Invalid server type. Please use 'samp' or 'mta'.")
            return
        
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
        await ctx.send(f"An error occurred while trying to add server: {e}")

@addserver.error
async def addserver_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Usage: T$addserver [samp or mta] [ip] [port]')
        
# Command to get players info
@bot.command()
async def players(ctx, address: str, port: int):
    try:
        with SampClient(address=address, port=port) as client:
            info = client.get_server_info()
            players = [client.name for client in client.get_server_clients_detailed()]
            server_name = info.hostname
            players_list = "\n".join(players)
            
            embed = discord.Embed(title="Server Players Info", color=discord.Color.green())
            embed.add_field(name="Server Name", value=info.hostname, inline=False)
            embed.add_field(name="Players", value=f"{info.players}/{info.max_players}", inline=False)
            embed.add_field(name="Player List", value=players_list, inline=False)
            
            await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred while trying to get players info: {e}")

@players.error
async def players_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Usage: T$players [ip] [port]')
        
# Read token from config file
with open("./config.json", 'r') as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["DISCORD_TOKEN"]

# Define the check loop
@tasks.loop(minutes=10)
async def checktop_loop(ctx):
    await checktop(ctx)
    
# Bot ready event
@bot.event
async def on_ready():
    activity = discord.Game(name="Orbx | Top Servers", type=3)
    await bot.change_presence(status=discord.Status.invisible, activity=activity)
    print("Bot is Online!")
    
    # Start the check loop
    guild = bot.get_guild(1150160889996136459)
    channel = guild.get_channel(1211807374885789726)
    checktop_loop.start(channel)

# Run the bot
bot.run(TOKEN)
