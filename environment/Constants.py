
from enum import IntEnum

RANKS = '23456789TJQKA'
SUITS = 'dchs'

# Example of 
# '2h'

class Action(IntEnum):
    """Allowed actions"""
    FOLD = 0
    CHECK = 1
    CALL = 2
    RAISE = 3
    SMALL_BLIND = 4
    BIG_BLIND = 5
    
class Stage(IntEnum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4
    END_HIDDEN = 5

class HandType(IntEnum):
    STRAIGHTFLUSH = 1
    FOUROFAKIND = 2
    FULLHOUSE = 3
    FLUSH = 4
    STRAIGHT = 5
    THREEOFAKIND = 6
    TWOPAIR = 7
    PAIR = 8
    HIGHCARD = 9
