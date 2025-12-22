import discord
import logging 
import os 
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

# Cogs 
COGS = (
    "cogs.dice"
)

class Moriza(commands.Bot): 
    def __init__(self):
        super().__init__(
            command_prefix = os.getenv("PREFIX"), 
            help_command = None, # REPLACE WITH CUSTOM LATER
            intents = intents, 
            )
        
        self.invite_link = os.getenv("INVITE_LINK") 

class HelpCommand(commands.HelpCommand):
    pass

bot = Moriza()

for cog in COGS:
    bot.load_extension(cog)

bot.run(os.dotenv("TOKEN"))