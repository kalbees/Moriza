import os
import random 
from enum import Enum

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

    def eval(self):
        return self.value

class Roll:
    def __init__(self, num_dice, sides):
        self.num_dice = num_dice
        self.sides = sides

        # Modifier flags
        self.exploding = False
        self.unique = False
        self.adv_dis = roll_mod.NONE
        self.keepdrop = None # Tuple, first value is the keep type, second is dice amount

    def eval(self):
        results = []
        dropped = []
        for i in range(self.num_dice): 
            roll = self.roll_dice(self.sides)
            if self.adv_dis != roll_mod.NONE:
                roll = self.apply_adv(roll, self.adv_dis)

        if self.exploding:
            exploded_rolls = self.explode(results)
            results.extend(exploded_rolls)

        if self.keepdrop != None: 
            results = self.drop(results, self.keepdrop[1], self.keepdrop[0])

        if self.unique:
            results = self.make_unique(results)

        return 
    
    def roll_dice(sides): 
        return random.randint(0, sides)

    def apply_adv(self, num, mod):
        roll = self.roll_dice(self.sides)
        if roll > num and mod == roll_mod.ADV: 
            return roll
        elif roll < num and mod == roll_mod.ADV:
            return num 
        elif roll > num and mod == roll_mod.DIS:
            return num
        else:
            return roll

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

class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class CompOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Group: 
    def __init__(self):
        pass