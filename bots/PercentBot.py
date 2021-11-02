"""Example1 player"""
from typing import Dict, Sequence

from bots.BotInterface import BotInterface
from environment.Constants import RANKS, Action, HandType, Stage
from environment.Observation import Observation
from utils.handValue import getHandPercent


class PercentBot(BotInterface):

    def __init__(self, name="percentBot"):
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        # use different strategy depending on pre or post flop (before or after community cards are delt)
        stage = observation.stage
        if stage == Stage.PREFLOP:
            return self.handlePreFlop(observation)
        else:
            return self.handlePostFlop(observation)
        
        # Unexpected!
        return Action.FOLD

    def handlePreFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, _ = getHandPercent(observation.myHand)
        # if my hand is top 40 percent: raise
        if handPercent < .40:
            return Action.RAISE
        # if my hand is top 60 percent: call
        elif handPercent < .60:
            return Action.CALL
        # else fold
        return Action.FOLD

    def handlePostFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is the best 5 card hand i can make out of all possible 5 card hands)
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        # if my hand is top 60 percent: raise
        if handPercent <= .60:
            return Action.RAISE
        # if my hand is top 80 percent: call
        elif handPercent <= .80:
            return Action.CALL
        # else fold
        return Action.FOLD

