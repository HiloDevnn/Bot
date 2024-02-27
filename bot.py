import discord
import json
from discord.ext import commands
from samp_client.client import SampClient

bot = commands.Bot(command_prefix='$', case_insensitive=True)

@bot.command() #SERVER INFO   ---   $players [ip] [port]
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


with open("./config.json", 'r') as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["DISCORD_TOKEN"]

@bot.event
async def on_ready():
    activity = discord.Game(name="Orbx Hosting#7091", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is Online!")

bot.run(TOKEN)
