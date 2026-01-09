import discord
import os 
from discord.ext import commands

DEFAULTROLE = "Dungeon Master"

# User and server settings cog class 
class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dm_role = DEFAULTROLE # Implement checking later
    
    # User commands 

    # Server-wide commands
    # Change or disable the default DM role
    @commands.command()
    async def dm_config_role(self, ctx, *, args): 
        embed = discord.Embed(color = "#6fc96f")
        # Set DM role if arguments are present 
        if args:
            # Check if user has admin perms
            if ctx.author.guild_permissions.administrator:
                # Set new role
                new_role = discord.utils.get(ctx.guild.roles, name = args)
                if new_role: 
                    self.dm_role = args
                    embed.description = f"DM role set to: {self.dm_role}"
                    await ctx.send(embed)
                else:
                    embed.description = f"The role {args} does not exist."
                    await ctx.send(embed)

        # Return current DM role if no arguments are added
        else:       
            embed.description = f"The current DM role is: {self.dm_role}"
            await ctx.send(embed)

    # Change or disable DM permissions for users
    @commands.command()
    async def dm_user_config():
        pass 