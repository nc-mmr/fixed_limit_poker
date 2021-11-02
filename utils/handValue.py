import pickle
from typing import Dict, List, Sequence, Tuple, Union
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
    ''' 
        Calculates the ranking of the input out of all possible hands in percent
            Parameters:
                hand (list[str]): player hand cards (['Ah','Jh'])
                board (list[str]): board cards (['Ah','Jh', 'Th'] or ['3s', '9c', '7h', '8d', 'Jc'] or ...) Optional
            returns:
                tuple of:
                    (float): hand rank as a percent out of all posible hands. low is better (0.234 or 0.8325 or ...)
                    (list[str]): cards in the best hand (['3s', '9c', '7h', '8d', 'Jc'])

        if board is not given:
            calculate the hand rank of the 2 player cards compared to all other 2 card hands   

            the card list returned with this is always just the cards given in 'hand'

            the 2 card hands are ranked based on the rankings found here: https://www.pokerhandrange.com/

            examples:
                ('As','Ah') is the best hand to have

                There are 6 combinations of this hand (2 aces), 0 combinations of better hands and 1326 combinations total of any 2 cards

                this function therefore returns 6/1326 = 0.0045248... = 0.45%

                Pocket aces is in the top 0.45% of all 2 card hands


                ('3s','2h') is the worst hand to have (in 1v1 poker)

                there are 12 combinations of this hand (3 and 2 not of the same suit), 1314 combinations of better hands and 1326 combinations total of any 2 cards

                this function therefore returns (12+1814)/1326 = 1... = 100%

                2 and 3 not of the same suit is in the top 100% of all 2 card hands
            
        
        if the board is given:
            calculates the best 5 card hand out of all input cards

            then calculates the rank of the 5 card hand out of all possible 5 card hands

            the card list returned with this is the 5 cards used to rank the hand


            NB! this ranking does not consider if a hand is possible given the board cards

            That is, even if the board cards do not make a flush possible, flushes are still considered part of 'all possible 5 card hands'

            So the best possible hand given the board cards might not even be in the top 15 % of hands

    '''
    if len(board) < 3:
        preflopHandType = _getPreflopHandType(hand)
        return rankings[preflopHandType], hand
    else:
        d_hand = [Card().new(c) for c in hand]
        d_board = [Card().new(c) for c in board]
        rank, cards = evaluator.evaluate(d_hand, d_board)
        percentage = evaluator.get_five_card_rank_percentage(rank)  # lower better here
        return percentage, [Card.int_to_pretty_str(c) for c in cards]


def getHandType(hand: List[str], board: List[str] = []) -> Union[ Tuple[str, List[str]], Tuple[HandType, List[str]] ]:
    '''
        calculates the hand type of the hand
            Parameters:
                hand (list[str]): player hand cards (['Ah','Jh'])
                board (list[str]): board cards (['Ah','Jh', 'Th'] or ['3s', '9c', '7h', '8d', 'Jc'] or ...) Optional
            returns:
                tuple of:
                    (HandType/str): hand type (STRAIGHTFLUSH or FULLHOUSE or TWOPAIR or ...) or ('KK' or 'K4s' or 'K4o' or ...)
                    (list[str]): cards in the best hand. (['3s', '9c', '7h', '8d', 'Jc'])

        if board is not given:
            Return the 2 card hand type

            the card list returned with this is always just the cards given in 'hand'

            examples:
                'KK' = pair of kings

                'K4s' = a king and a 4 in the same suit

                'KTo' = a king and a 10 not in the same suit

        if the board is given:
            return the best 5 card poker hand type from the input cards

            the card list returned with this is the 5 cards used in the hand type

            example:
                hand = ['3s', 'Ah']

                board = ['As', '7s', 'Kh', '2d', 'Kc']

                returns (HandType.TWOPAIR, ['Ah', 'As', '7s', 'Kh', 'Kc'])
        
    '''
    if len(board) < 3:
        return _getPreflopHandType(hand), hand
    else:    
        d_hand = [Card().new(c) for c in hand]
        d_board = [Card().new(c) for c in board]
        rank, cards = evaluator.evaluate(d_hand, d_board)
        return HandType(evaluator.get_rank_class(rank)), [Card.int_to_pretty_str(c) for c in cards]


def getLongestStraight(hand: List[str], board: List[str]) -> Tuple[int, str, str]:
    '''
        calculates the longest number of consecutive ranked cards in the input
            Parameters:
                hand (list[str]): player hand cards (['Ah','Jh'])
                board (list[str]): board cards (['Ah','Jh', 'Th'] or ['3s', '9c', '7h', '8d', 'Jc'] or ...)
            returns:
                Tuple of:
                    (int): number of consecutive ranked cards
                    (str): start rank of consecutive cards
                    (str): end rank of consecutive cards

        NB! this function only returns the first found start and end ranks if there are mutiple consecutive ranked cards of the same length
    '''
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

def getHighestSuitCount(hand: List[str], board: List[str]) -> Tuple[int, str]:
    '''
        calculates number of cards of each suit and returns the one with highest count
            Parameters:
                hand (list[str]): player hand cards (['Ah','Jh'])
                board (list[str]): board cards (['Ah','Jh', 'Th'] or ['3s', '9c', '7h', '8d', 'Jc'] or ...)
            returns:
                Tuple of:
                    (int): number of cards with suit 'x'
                    (str): the suit 'x' with the highest count

        NB! this function only returns the first suit if there are mutiple suits with the same count
    '''
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
    '''
        calculates the hand type of the board
            Parameters:
                board (list[str]): board cards (['Ah','Jh', 'Th'] or ['3s', '9c', '7h', '8d', 'Jc'] or ...)
            returns:
                (HandType) hand type (THREEOFAKIND or PAIR or TWOPAIR or ...)
        
        Calculates the handtype of the board.
        
        This is usefull to calculate if your hand is part of the best hand.
        example:
            board = ['4s', '7s', 'Kh', 'Kc']
            returns HandType.PAIR
    '''
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

