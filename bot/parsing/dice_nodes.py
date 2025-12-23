import os
import random 
from enum import Enum
from .dice_result import RollResult

# Modifier enums
class roll_mod(Enum):
    NONE = 0
    ADV = 1
    DIS = 2

class keep_type(Enum): 
    HIGHEST = 0
    LOWEST = 1

class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return RollResult(total=self.value, rolls=[self.value], raw_rolls=[self.value])

class Roll:
    def __init__(self, num_dice, sides):
        self.num_dice = num_dice
        self.sides = sides

        # Modifier flags
        self.exploding = False
        self.unique = False
        self.adv_dis = roll_mod.NONE
        self.keepdrop = None # Tuple, first value is the keep type, second is dice amount

    def evaluate(self):
        init_results = []
        results = []
        dropped = []

        # Roll raw results 
        for i in range(self.num_dice): 
            init_roll = self.roll_dice(self.sides)
            if self.adv_dis != roll_mod.NONE:
                applied_roll = self.apply_adv(init_roll, self.adv_dis) 
                dropped.append(applied_roll[1])
                init_results.append(applied_roll[0])
            else: 
                init_results.append(init_roll)

        # Apply relevant flags and add to results
        if self.exploding:
            exploded_rolls = self.explode(init_results)
            results.extend(exploded_rolls)

        if self.keepdrop != None: 
            results = self.drop(init_results, self.keepdrop[1], self.keepdrop[0])

        if self.unique:
            results = self.make_unique(init_results)

        # Calculate final roll from results
        final_result = 0
        for x in results: 
            final_result += x
        
        # Create dictionary for modifiers
        modifiers = {
            "Exploding": self.exploding,
            "Unique": self.unique,
            "Advantage/Disadvantage": self.adv_dis,
            "Keep/Drop": self.keepdrop 
        }

        return RollResult(total=final_result, rolls=results, raw_rolls=init_results, dropped=dropped, flags=modifiers)
    
    def roll_dice(sides): 
        return random.randint(1, sides)

    # Apply adv/dis to roll, return tuple w/ second number being the dropped roll
    def apply_adv(self, num, mod):
        reroll = self.roll_dice(self.sides)
        if reroll > num and mod == roll_mod.ADV: 
            return (reroll, num)
        elif reroll < num and mod == roll_mod.ADV:
            return (num, reroll) 
        elif reroll > num and mod == roll_mod.DIS:
            return (num, reroll)
        else:
            return (reroll, num) 

    def explode(self, rolls): 
        exploded_rolls = []
        for r in rolls: 
            if r == self.sides:
                while exploded_rolls[-1] == self.sides: 
                    exploded_rolls.append(self.roll_dice(self.sides))
        return exploded_rolls

    def drop(self, rolls, num, type):
        kept_rolls = []
        if type == keep_type.HIGHEST:
            while len(kept_rolls) != num: 
                kept_rolls.append(max(rolls))
                rolls.remove(max(rolls))
                return kept_rolls
        else: 
            while len(kept_rolls != num):
                kept_rolls.append(min(rolls))
                rolls.remove(min(rolls))
                return kept_rolls

    def make_unique(self, rolls): 
        seen = set()
        for r in rolls: 
            if r in seen: 
                new_roll = r
                while new_roll in seen: 
                    new_roll = self.roll_dice(self.sides)
                r = new_roll
                seen.add(r)
            else:
                seen.add(r)
        return rolls 

class UnaryOp:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    
    def evaluate(self):
        value = self.operand.evaluate()
        total = 0
        if self.op == "-":
            total = -value
        elif self.op == "+":
            total = value
        else:
            raise ValueError(f"Unknown unary operator: {self.op}")
        
        return RollResult(total=total, rolls=[total], raw_rolls=[value])

class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):
        # Calculate totals
        left_total = self.left.evalaute().total 
        right_total = self.right.evaluate().total
        final_total = 0

        if self.op == "+":
            final_total = left_total + right_total
        elif self.op == "-":
            final_total = left_total - right_total
        elif self.op == "*":
            final_total = left_total * right_total
        elif self.op == "/":
            final_total = left_total // right_total
        else:
            raise ValueError(f"Unknown binary operator: {self.op}")
        
        return RollResult(total=final_total, parts=[self.left.evaluate(), self.right.evaluate()], op=self.op)

class CompOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def evaluate(self):
        left_total = self.left.evaluate().total
        right_total = self.right.evaluate().total

        if self.op == ">":
            return left_total > right_total
        elif self.op == "<":
            return left_total < right_total
        elif self.op == "==":
            return left_total == right_total
        else: 
            raise ValueError(f"Unknown comparison operator: {self.op}")

class Group: 
    def __init__(self, expr):
        self.expr = expr
    
    def evaluate(self):
        return self.expr.evaluate() 