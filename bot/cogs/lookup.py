import discord 
import os
import aiohttp
import django
import rest_framework 
from discord.ext import commands

# D&D Lookup Cog 
class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def close_session(self): 
        self.bot.loop.create_task(self.session.close())

    # Monster Lookup
    @commands.Command(name = "monster")
    async def monster_lookup(self, ctx, *, name: str):
        try:
            monster_data = self._lookup(category = "monsters", search_term = name)
        except Exception as e: 
            return await ctx.send(f"Lookup failed: {e}")

        embed = discord.Embed(
            title = monster_data["name"],
            color = "#5a43de"
        )

    # Conditions Lookup
    @commands.Command(name = "condition")
    async def conditions_lookup(self, ctx, *, name: str):
        try:
            condition_data = self._lookup(category = "conditions", search_term = name)
        except Exception as e: 
            return await ctx.send(f"Lookup failed: {e}")

        embed = discord.Embed(
            title = condition_data["name"],
            color = "#5a43de"
        )

    # Class Lookup 
    @commands.Command(name = "class")
    async def class_lookup(self, ctx, *, name: str):
        try:
            class_data = self._lookup(category = "classes", search_term = name)
        except Exception as e: 
            return await ctx.send(f"Lookup failed: {e}")

        embed = discord.Embed(
            title = class_data["name"],
            color = "#5a43de"
        )

    # Backgrounds Lookup
    @commands.Command(name = "background") 
    async def background_lookup(self, ctx, *, name: str): 
        try:
            bg_data = self._lookup(category = "backgrounds", search_term = name)
        except Exception as e: 
            return await ctx.send(f"Lookup failed: {e}")

        embed = discord.Embed(
            title = bg_data["name"],
            color = "#5a43de"
        )

    # Feats Lookup
    @commands.Command(name = "feat")
    async def feat_lookup(self, ctx, *, name: str):
        try:
            feat_data = self._lookup(category = "feats", search_term = name)
        except Exception as e: 
            return await ctx.send(f"Lookup failed: {e}")
        
        embed = discord.Embed(
            title = feat_data["name"],
            color = "#5a43de"
        )

    # Spells Lookup 
    @commands.Command(name = "spell")
    async def spell_lookup(self, ctx, *, name: str):
        try:
            spell_data = self._lookup(category = "spells", search_term = name)
        except Exception as e: 
            return await ctx.send(f"Lookup failed: {e}")

        embed = discord.Embed(
            title = spell_data["name"],
            color = "#5a43de"
        )

        # Format components 
        verbal = "V" if spell_data["verbal"] == True else None
        somatic = "S" if spell_data["somatic"] == True else None
        material = "M" if spell_data["material"] == True else None
        components = ", ".join([verbal, somatic, material])

        # Format embed 
        desc = f"""*Level {spell_data["level"]} {spell_data["school"]["name"]} {"(ritual)" if spell_data["ritual"] == True else None}*\n
                    **Casting Time:** {spell_data["cast_time"]}\n
                    **Range:** {spell_data["range_text"]}\n
                    **Components: {components}\n** 
                    **Duration:** {spell_data["duration"]}\n
                    {spell_data["desc"]}"""
        
        embed.description = desc

        return ctx.send(embed)
    
    # Lookup helper 
    async def _lookup(self, category, search_term):
        # Setup search 
        url = f"{self.api_base}/search/{category}/"
        params = {"search": search_term}

        # Call Open5e
        async with self.session.get(url, params = params) as response:
            # Error handling
            if response.status == 400: 
                raise ValueError("Missing search parameter")
            if response.status == 404:
                raise LookupError("Search category does not exist")
            if response.status != 200: 
                raise RuntimeError("Open5e External API error")
        
        return await response.json() 