from caf import *
import discord
import os
import requests
import aiohttp
import asyncio
import time
import pymongo
from config import *
from pymongo import MongoClient
from discord.ext import tasks
from discord import ui
import datetime
from datetime import datetime, timezone, timedelta
from discord.ext import commands
import json
from discord.ext import commands



bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Der Bot ist bereit')




@bot.tree.command(description='Manages a roblox player')
async def manage_user(interaction: discord.Interaction, username:str, userid:int):
    if checkusername(username) is False:
        return await interaction.response.send_message(f'The username `{username}` is invalid or the user is banned from roblox.')
    
    await interaction.response.send_message(f'Managing {username}', view=manageui(interaction.user, username, userid))








@bot.command()
#@commands.is_owner()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send(':ok_hand:')




bot.run(token)