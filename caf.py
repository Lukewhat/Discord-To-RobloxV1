import requests
from discord import ui
import discord
import json
from pymongo import MongoClient
from config import *



client = MongoClient(mongourl)



def CheckBan(username:str) -> bool:
    client.server_info()
    database = client['rbxbandb']
    collection = database['bans']
    if collection.find_one({'Username': username}):
        return True
    else:
        return False



def AddUserToBanDb(username:str, userid:int, reason:str):
    client.server_info()
    database = client['rbxbandb']
    collection = database['bans']
    collection.insert_one({'Username': f'{username}', 'userid': f'{userid}', 'reason': f'{reason}'})



def RemoveUserFromBanDb(username:str):
    client.server_info()
    database = client['rbxbandb']
    collection = database['bans']
    collection.delete_one({'Username': f'{username}'})



def checkusername(username:str) -> bool:
    r = requests.get(f'https://api.newstargeted.com/roblox/users/v2/user.php?username={username}')
    rj = r.json()
    if 'error' in rj:
        return False
    else:
        return True




class banmodal(ui.Modal, title='Reason for ban.'):
    
    reason = ui.TextInput(label='Reason')

    def __init__(self, username:str, userid:int):
        super().__init__()
        self.username = username
        self.userid = userid

    async def on_submit(self, interaction: discord.Interaction):
        AddUserToBanDb(self.username, self.userid, self.reason)
        await interaction.response.send_message(f'Successfully banned `{self.username}`')




class manageui(discord.ui.View):
    def __init__(self, invoker:discord.Member, username:str, userid:int):
        super().__init__()
        self.invoker = invoker
        self.username = username
        self.userid = userid


    @discord.ui.button(label="Ban", style=discord.ButtonStyle.blurple)
    async def banuser(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.invoker.id:
            if CheckBan(self.username) == False:
                await interaction.response.send_modal(banmodal(self.username, self.userid))
            else:
                await interaction.response.send_message(f'`{self.username}` is already banned.')


    @discord.ui.button(label="UnBan", style=discord.ButtonStyle.blurple)
    async def unbanuser(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.invoker.id:
            if CheckBan(self.username) == True:
                await interaction.response.send_message(f'Unbanned `{self.username}`')
                RemoveUserFromBanDb(self.username)
            else:
                await interaction.response.send_message(f'`{self.username}` is not banned.')


    @discord.ui.button(label="Cancel Operation", style=discord.ButtonStyle.blurple)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.invoker.id:
            await interaction.message.delete()