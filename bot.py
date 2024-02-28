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
            data = json.load(file)
        
        samp_servers = data.get('samp_servers', [])
        
        # Create a temporary list to store server info
        temp_list = []
        
        for server in samp_servers:
            ip = server['ip']
            port = server['port']
            info = await get_server_info(ip, port)
            if info:
                temp_list.append({'hostname': info.hostname, 'players': info.players, 'max_players': info.max_players})
        
        # Sort the servers based on the number of players
        sorted_servers = sorted(temp_list, key=lambda x: x['players'], reverse=True)
        
        # Get the top 10 servers
        top_10_servers = sorted_servers[:10]
        
        # Create embeds
        embed1 = discord.Embed(title="Orbx Hosting TOP 10 SA:MP Servers", color=0xf1bc48)
        embed1.set_image(url="https://media.discordapp.net/attachments/1172640694939168808/1188495474525741158/20231224_155630.jpg?ex=659abbaa&is=658846aa&hm=47d25a69bfcc1a676ac6d2f6a323d1a21ba09dcd17318f85edacd8e468cacdae&")
        
        # Emoji dictionary
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
        
        # Add server info to embed1
        description1 = ""
        for idx, server in enumerate(top_10_servers, start=1):
            emoji = num_to_emoji.get(idx, '⁉️')
            description1 += f"{emoji} ```{server['players']}/{server['max_players']}``` | {server['hostname']}\n"
        embed1.description = description1
        
        # Create embed2
        embed2 = discord.Embed(title="", description="4600 Players Are Now Connected To All This Orbx Servers\nNext Refresh In || 0 minutes ||", color=0xf1bc48)
        embed2.set_footer(text="Orbx Status | All rights Reserved 2023 - 2024", icon_url="https://cdn.discordapp.com/attachments/1172640694939168808/1188462447921733703/20231224_132801.jpg?ex=659a9ce8&is=658827e8&hm=3038be5bee65b6d90313e270b416010e8bbc4f4f43439c13d0496cac886fe673&")
        
        # Send both embeds in the same message
        await ctx.send(embeds=[embed1, embed2])
        
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while trying to get server info.")

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
