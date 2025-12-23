import os 

class RollResult:
    def __init__(
            self, 
            total: int, 
            rolls: list[int], 
            raw_rolls: list[int], 
            dropped: list[int], 
            flags: dict,
            modifiers: list[int],
            parts,
            op):
        
        self.total = total                  # final result total 
        self.rolls = rolls or []            # every individual accepted roll (used for calculating total)
        self.raw_rolls = raw_rolls or []    # all rolls, kept and dropped   
        self.dropped = dropped or []        # all dropped rolls
        self.flags = flags or {}            # adv, dis, explode, unique 
        self.modifiers = modifiers or []    # solid numbers added to a roll (i.e. +2, -1)
        self.parts = parts or []            # the roll's children in the tree
        self.op = op or None                # any main operator included in the role

    # Return all parts/children as a list 
    def get_all_rolls(self):
        rolls = []
        for x in self.parts:
            rolls.extend(x.get_all_rolls())
        if self.rolls:
            rolls.append(self)
        return rolls