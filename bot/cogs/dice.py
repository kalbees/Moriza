import discord 
import random
import math
import os 
from lark import Lark
from discord.ext import commands
from parsing.dice_transformer import DiceTransformer

# Dice roller cog class 
class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.parser = Lark()
        self.transformer = DiceTransformer()
    
    # Commands for normal dice rolling
    @commands.command()
    async def roll(self, ctx, *, expr: str):
        try:
            result_tree = self.parser.parse(expr)
            ast = self.transformer.transform(result_tree)
            result = ast.evaluate()
        except Exception as e: 
            return await ctx.send(f"Roll error: invalid dice expression: {e}")
        
        # Format the parse tree into embed
        output = self._formatRoll(result)
        return await ctx.send(output)


    @commands.command()
    async def rollstats(self, ctx):
        result_tree = self.parser.parse("4d6kh3")

        # Format the parse tree into embed 
        

    # Commands for math and distribution
    @commands.command()
    async def find_avg(self, ctx, *, expr: str):
        try:
            result_tree = self.parser.parse(expr)
        except Exception as e:
            return await ctx.send(f"Roll error: invalid dice expression: {e}")

    @commands.command()
    async def find_max(self, ctx): 
        pass

    # Commands for other systems of randomization
    @commands.command()
    async def flip(self, ctx):
        embed = discord.Embed(
            color="#63daf2"
        )
        result = random.choice(["Heads", "Tails"])
        if result == "Heads": 
            embed.description = "You got heads!"
            await ctx.send(embed)
        else:
            embed.description = "You got tails!"
            await ctx.send(embed)
    
    @commands.command()
    async def multiflip(self, ctx, num: int):
        embed = discord.Embed(
            color="#63daf2"
        )
        results = []
        for i in range(int):
            results.append(random.choice["Heads", "Tails"])
        embed.description = "Your results are: " + ", ".join(results)
        await ctx.send(embed)
    
    # Helpers
    def _formatRoll(result):
        pass 