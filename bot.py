import discord
import json
from discord.ext import commands, tasks
from samp_client.client import SampClient
import gamedig

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='$', case_insensitive=True, intents=intents)

# Function to get server info
async def get_server_info(address, port):
    try:
        with SampClient(address=address, port=port) as client:
            info = client.get_server_info()
            return info
    except Exception as e:
        print(f"Error getting server info for {address}:{port}: {e}")
        return None

async def get_mta_server_info(ip, port):
    try:
        state = await gamedig.query(
            type="mtasa",
            host=ip,
            port=port
        )
        return state
    except Exception as e:
        print(f"Error getting MTA server info for {ip}:{port}: {e}")
        return None
        
        
# Command to check server info
@bot.command()
async def check(ctx):
    try:
        with open('servers.json', 'r') as file:
            data = json.load(file)
        
        samp_servers = data.get('samp_servers', [])
        mta_servers = data.get('mta_servers', [])
        
        samp_temp_list = []
        mta_temp_list = []
        
        for server in samp_servers:
            ip = server['ip']
            port = server['port']
            info = await get_server_info(ip, port)
            if info:
                samp_temp_list.append({'hostname': info.hostname, 'players': info.players, 'max_players': info.max_players})
        
        for server in mta_servers:
            ip = server['ip']
            port = server['port']
            info = await get_mta_server_info(ip, port)  # تحديث هنا لاستخدام الدالة الجديدة
            if info:
                mta_temp_list.append({'hostname': info.name, 'players': info.raw.numplayers, 'max_players': info.maxplayers})
        
        total_samp_players = sum(server['players'] for server in samp_temp_list)
        total_mta_players = sum(server['players'] for server in mta_temp_list)
        
        sorted_samp_servers = sorted(samp_temp_list, key=lambda x: x['players'], reverse=True)
        sorted_mta_servers = sorted(mta_temp_list, key=lambda x: x['players'], reverse=True)
        
        top_10_samp_servers = sorted_samp_servers[:10]
        top_10_mta_servers = sorted_mta_servers[:10]
        
        embed1_samp = discord.Embed(title="<:orbx:1188474625429082142> Orbx Hosting TOP 10 SA:MP Servers", color=0xf1bc48)
        embed1_samp.set_image(url="https://media.discordapp.net/attachments/1172640694939168808/1188495474525741158/20231224_155630.jpg?ex=659abbaa&is=658846aa&hm=47d25a69bfcc1a676ac6d2f6a323d1a21ba09dcd17318f85edacd8e468cacdae&")
        
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
        
        description1_samp = ""
        for idx, server in enumerate(top_10_samp_servers, start=1):
            emoji = num_to_emoji.get(idx, '⁉️')
            description1_samp += f"{emoji} ```{server['players']}/{server['max_players']}``` | {server['hostname']}\n"
        
        embed1_samp.description = description1_samp
        
        embed1_mta = discord.Embed(title="<:orbx:1188474625429082142> Orbx Hosting TOP 10 MTA Servers", color=0xf1bc48)
        embed1_mta.set_image(url="https://media.discordapp.net/attachments/1172640694939168808/1188495474525741158/20231224_155630.jpg?ex=659abbaa&is=658846aa&hm=47d25a69bfcc1a676ac6d2f6a323d1a21ba09dcd17318f85edacd8e468cacdae&")
        
        description1_mta = ""
        for idx, server in enumerate(top_10_mta_servers, start=1):
            emoji = num_to_emoji.get(idx, '⁉️')
            description1_mta += f"{emoji} ```{server['players']}/{server['max_players']}``` | {server['hostname']}\n"
        
        embed1_mta.description = description1_mta
        
        total_players_text = f"<:orbx:1188474625429082142> {total_samp_players + total_mta_players} Players Are Now Connected To All These Orbx Servers.\nNext Refresh in: || 5 seconds || ⏱️"
        embed2 = discord.Embed(title="", description=total_players_text, color=0xf1bc48)
        embed2.set_footer(text="Orbx Hosting | All rights Reserved 2023 - 2024", icon_url="https://cdn.discordapp.com/attachments/1172640694939168808/1188462447921733703/20231224_132801.jpg?ex=659a9ce8&is=658827e8&hm=3038be5bee65b6d90313e270b416010e8bbc4f4f43439c13d0496cac886fe673&")
        embed2.set_image(url="https://media.discordapp.net/attachments/1172640694939168808/1188495474525741158/20231224_155630.jpg?ex=659abbaa&is=658846aa&hm=47d25a69bfcc1a676ac6d2f6a323d1a21ba09dcd17318f85edacd8e468cacdae&")
        
        guild = bot.get_guild(1184971073645715487)
        channel = guild.get_channel(1206679721237155890)
        
        message = await channel.fetch_message(1212480958746460202)
        
        await message.edit(embeds=[embed1_samp, embed1_mta, embed2])
        
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while trying to update the message.")


# Read token from config file
with open("./config.json", 'r') as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["DISCORD_TOKEN"]

# Define the check loop
@tasks.loop(seconds=5)
async def check_loop(ctx):
    await check(ctx)
    
# Bot ready event
@bot.event
async def on_ready():
    activity = discord.Game(name="Orbx | Top Servers", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is Online!")
    
    # Start the check loop
    guild = bot.get_guild(1184971073645715487)
    channel = guild.get_channel(1206679721237155890)
    check_loop.start(channel)

# Run the bot
bot.run(TOKEN)
