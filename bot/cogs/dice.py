import discord 
import random
import math
import os 
from lark import Lark
from discord.ext import commands
from enum import Enum
from parsing.dice_nodes import roll_mod, keep_type
from parsing.dice_transformer import DiceTransformer
from parsing.dice_result import RollResult

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
        output = self._formatRoll(result, expr)
        return await ctx.send(output)

    @commands.command()
    async def rollstats(self, ctx):
        stats = []
        # Roll for six different stats 
        for i in range(6):
            result_tree = self.parser.parse("4d6kh3")
            ast = self.transformer.transform(result_tree)
            result = ast.evaluate()
            stats.append(result)

        # Format the parse tree into embed 
        output = self._formatStats(stats)
        return await ctx.send(output)

    # Commands for math and distribution
    @commands.command()
    async def find_avg(self, ctx, *, expr: str):
        try:
            result_tree = self.parser.parse(expr)
            ast = self.transformer.transform(result_tree)
            result = ast.evaluate()
        except Exception as e:
            return await ctx.send(f"Roll error: invalid dice expression: {e}")

    @commands.command()
    async def find_max(self, ctx, *, expr: str):
        try:
            result_tree = self.parser.parse(expr)
            ast = self.transformer.transform(result_tree)
            result = ast.evaluate() 
        except Exception as e:
            return await ctx.send(f"Roll error: invalid dice expression: {e}") 
        pass

    @commands.command()
    async def find_min(self, ctx, *, expr: str):
        try:
            result_tree = self.parser.parse(expr)
        except Exception as e:
            return await ctx.send(f"Roll error: invalid dice expression: {e}")
        pass

    # Commands for other systems of randomization
    @commands.command()
    async def flip(self, ctx):
        embed = discord.Embed(
            color="#63daf2"
        )
        result = random.choice(["Heads", "Tails"])
        if result == "Heads": 
            embed.description = "🪙 You got heads!"
            await ctx.send(embed)
        else:
            embed.description = "🪙 You got tails!"
            await ctx.send(embed)
    
    @commands.command()
    async def multiflip(self, ctx, num: int):
        embed = discord.Embed(
            color = "#63daf2"
        )
        results = []
        for i in range(num):
            results.append(random.choice["Heads", "Tails"])
        embed.description = "🪙 Your results are: " + ", ".join(results)
        await ctx.send(embed)
    
    # Helpers
    def _formatRoll(self, result, expr: str):
        embed = discord.Embed(
            title = f"🎲 Rolling {expr}...",
            color = "#F54927"
        )
        roll_lines = []

        # Get all children from roll
        all_nodes = result.get_all_rolls()
        leaf_nodes = [x for x in all_nodes if x.results]
        
        # Format every child  
        for y in leaf_nodes: 
            roll_lines.append(self._formatRollLine(y, expr))
            if y.flags.get("Advantage/Disadvantage") != roll_mod.NONE:
                roll_lines.append("Advantage/Disadvantage: " + y.flags.get("Advantage/Disadvantage").name.title())

        # Add total at the end
        roll_lines.append("--- \n" + "Total: " + str(result.total))

        # Add to embed
        embed.description = "\n".join(roll_lines)

        return embed

    def _formatRollLine(roll: RollResult, expr: str): 
        rolls = []
        for x in roll.dropped: 
            rolls.append(f"~~{x}~~")
        for y in roll.results: 
            rolls.append(y)
        return f"Rolls ({expr}): " + ", ".join(rolls)

    def _formatStats(results):
        embed = discord.Embed(
            title = "🎲 Rolled Stats (4d6kh3)",
            color = "#F54927"
        )
        
        # Add stats to description
        str_stats = ""
        for i in range(6):
            # Format every stat, crossing out dropped rolls 
            stat = "("
            stat += ", ".join(results[i].raw_rolls)
            dropped_num = "~~" + results[i].dropped[0] + "~~"
            stat.replace(results[i].dropped[0], dropped_num)
            stat += ")"
            str_stats += stat + "\n"
    
        # Add total to description
        total_points = 0
        for x in results:
            total_points += x.total
        str_stats += "--- \n" + "Total: " + str(total_points)
        embed.description = str_stats

        return embed