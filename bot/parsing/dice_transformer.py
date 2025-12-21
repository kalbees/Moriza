import os
from lark import Transformer
from .dice_nodes import (
    roll_mod,
    keep_type,
    Number,
    Roll,
    UnaryOp,
    BinaryOp,
    CompOp,
    Group
)
from enum import Enum

class DiceTransformer(Transformer): 
    # Expression transformers 
    def NUMBER(self, token):
        return Number(self, int(token))
    
    def start(self, children):
        """
        start: expr 
        """
        return children[0]

    def expr(self, children):
        """
        expr: comp_expr
        """ 
        return children[0]
    
    def comp_expr(self, children):
        """
        comp_expr: sum_expr (COMP_OP sum_expr)*
        """ 
        if len(children) == 1:
            return children[0]

        node = children[0]
        for i in range(1, len(children), 2):
            op = children[i]
            right = children[i + 1]
            node = CompOp(node, op, right)
        
        return node
    
    def sum_expr(self, children):
        if len(children) == 1: 
            return children[0]
        
        node = children[0]
        for i in range(1, len(children), 2):
            op = children[i]
            right = children[i + 1]
            node = BinaryOp(node, op, right)
        
        return node 

    def mul_expr(self, children):
        if len(children) == 1: 
            return children[0]
        
        node = children[0]
        for i in range(1, len(children), 2):
            op = children[i]
            right = children[i + 1]
            node = BinaryOp(node, op, right)
        
        return node 

    def unary_expr(self, children): 
        if len(children) == 1: 
            return children[0]
        
        op = children[0]
        operand = children[1]
        node = UnaryOp(op, operand)

        return node 

    def group(self, children):
        return Group(children[0])

    def roll(self, children): 
        """
        roll: dice modifiers*
        """
        die = children[0]
        modifiers = children[1:]

        for mod in modifiers: 
            mod.apply(die)
        
        # check if unique is possible 
        if die.unique and die.num_dice > die.sides: 
            raise ValueError(f"Cannot roll {die.num_dice} unique results from d{die.sides}.")
        
        return die
    
    def dice(self, children): 
        """
        dice: NUMBER? DIE (NUMBER | "%")
        """
        if len(children) == 1:
            num_dice = 1
            sides = children[0]
        else:
            num_dice = children[0]
            sides = children[1]
        
        return Roll(num_dice, sides)
    
    # Modifier handlers, used to apply modifier objects

    def explode(self, _):
        return _ExplodeMod()
    
    def unique(self, _):
        return _UniqueMod()
    
    def adv_dis(self, children):
        return _AdvDisMod(children[0].value)
    
    def keepdrop(self, children): 
        return _KeepDropMod(children[0].value, children[1].value)

# Modifier objects
class _ExplodeMod(): 
    def apply(self, roll_node):
        roll_node.exploding = True

class _UniqueMod(): 
    def apply(self, roll_node): 
        roll_node.unique = True

class _AdvDisMod():
    def __init__(self, mod_type):
        self.mod_type = mod_type
    
    def apply(self, roll_node):
        roll_node.adv_dis = self.keep_type

class _KeepDropMod():
    def __init__(self, type, count):
        self.type = type
        self.count = count 

    def apply(self, roll_node): 
        roll_node.keepdrop(self.type, self.count)
