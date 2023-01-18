import datetime
import os
import disnake

from disnake.ext import commands

bot = commands.Bot(command_prefix="/", intents=disnake.Intents.all())
bot.remove_command('help')


@bot.command()
@commands.is_owner()
async def load(message, extension):
    channel = bot.get_channel(1059647120761700423)
    bot.load_extension(f"cogs.{extension}")
    embed = disnake.Embed(
        title=f"{extension}",
        colour=disnake.Colour.dark_gray(),
        description="Успешно загружен!"
    )
    await channel.send(embed=embed)


@bot.command()
@commands.is_owner()
async def unload(message, extension):
    channel = bot.get_channel(1059647120761700423)
    bot.unload_extension(f"cogs.{extension}")
    embed = disnake.Embed(
        title=f"{extension}",
        colour=disnake.Colour.dark_gray(),
        description="Успешно выгружен!"
    )
    await channel.send(embed=embed)


@bot.command()
@commands.is_owner()
async def reload(message, extension):
    channel = bot.get_channel(1059647120761700423)
    bot.reload_extension(f"cogs.{extension}")
    embed = disnake.Embed(
        title=f"{extension}",
        colour=disnake.Colour.dark_gray(),
        description="Успешно перезагружен!"
    )
    await channel.send(embed=embed)


for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


# Старт бота
token = open("token.txt", "r").readline()
bot.run(token)
