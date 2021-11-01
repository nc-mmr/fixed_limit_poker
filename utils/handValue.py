import pickle
from typing import Dict, List, Sequence, Tuple
from collections import defaultdict
from environment.Constants import RANKS, SUITS, HandType
from utils.deuces.card import Card
from utils.deuces.evaluator import Evaluator

evaluator = Evaluator()
with open('./utils/preflopHandRankings.pckl', 'rb') as rankingsFile:
    rankings = pickle.load(rankingsFile)

def _getPreflopHandType(hand: Sequence[str]) -> str:
    hand = sorted(hand, key=lambda x: RANKS.index(x[0]), reverse=True)

    if hand[0][0] == hand[1][0]:
        return hand[0][0] + hand[1][0]
    elif hand[0][1] == hand[1][1]:
        return hand[0][0] + hand[1][0] + 's'
    else:
        return hand[0][0] + hand[1][0] + 'o'

def getHandPercent(hand: Sequence[str], board: Sequence[str] = []) -> Tuple[float, List[str]]:
    if len(board) == 0:
        preflopHandType = _getPreflopHandType(hand)
        return rankings[preflopHandType], hand
    else:
        d_hand = [Card().new(c) for c in hand]
        d_board = [Card().new(c) for c in board]
        rank, cards = evaluator.evaluate(d_hand, d_board)
        percentage = evaluator.get_five_card_rank_percentage(rank)  # lower better here
        return percentage, [Card.int_to_pretty_str(c) for c in cards]


def getHandType(hand: List[str], board: List[str] = []) -> Tuple[HandType, List[str]]:
    if len(board) == 0:
        return _getPreflopHandType(hand), hand
    else:    
        d_hand = [Card().new(c) for c in hand]
        d_board = [Card().new(c) for c in board]
        rank, cards = evaluator.evaluate(d_hand, d_board)
        return HandType(evaluator.get_rank_class(rank)), [Card.int_to_pretty_str(c) for c in cards]

# 2d 3d 4d
# 
def getLongestStraight(hand: List[str], board: List[str] = []) -> Tuple[int, str, str]:
    cardRanks = [RANKS.index(c[0]) for c in hand + board]
    if RANKS.index('A') in cardRanks:
        cardRanks.append(-1) # add low ace
    cardRanksSet = set(cardRanks)

    ans = 0
    startRank = 0
    for rank in cardRanksSet:  
        j = rank + 1

        while j in cardRanksSet:
            j = j + 1

        if j - rank > ans:
            ans = j - rank
            startRank = rank
    
    if startRank == -1:
        return ans, "A", RANKS[startRank + ans - 1]
    return ans, RANKS[startRank], RANKS[startRank + ans - 1]

def getHighestSuitCount(hand: List[str], board: List[str] = []) -> Tuple[int, str]:
    suits = [c[1] for c in hand + board]
    highestCount = 0
    highestCountSuit = ''
    for s in SUITS:
        count = suits.count(s)
        if count > highestCount:
            highestCount = count
            highestCountSuit = s
    return highestCount, highestCountSuit

def getBoardHandType(board: List[str]) -> HandType:
    if len(board) >= 5:
        return getHandType(board[:2], board[2:])[0]
    else:
        ranks = [c[0] for c in board]
        counts = defaultdict(lambda: 1)
        for i in range(len(ranks)-1):
            if ranks[i] == ranks[i+1]:
                counts[ranks[i]] += 1
        counts = list(counts.values())
        if len(counts) > 1:
            return HandType.TWOPAIR
        elif len(counts) == 1:
            if counts[0] == 2:
                return HandType.PAIR
            elif counts[0] == 3:
                return HandType.THREEOFAKIND
            elif counts[0] == 4:
                return HandType.FOUROFAKIND
    return HandType.HIGHCARD

