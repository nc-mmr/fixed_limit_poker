"""Percent bot player"""
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action, Stage
from environment.Observation import Observation
from utils.handValue import getHandPercent


class PercentBot(BotInterface):
    """
    PercentBot calculates how good it's hand is compared to all the hands that exist in poker.

    It never considers what it's opponent is doing, 
    nor does it consider what might have happened earlier in the round.
    """

    def __init__(self, name="percentBot"):
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        # use different strategy depending on pre or post flop (before or after community cards are delt)
        stage = observation.stage
        if stage == Stage.PREFLOP:
            return self.handlePreFlop(observation)

        return self.handlePostFlop(observation)

    def handlePreFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, _ = getHandPercent(observation.myHand)
        # if my hand is top 20 percent: raise
        if handPercent < .20:
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
        # if my hand is top 30 percent: raise
        if handPercent <= .30:
            return Action.RAISE
        # if my hand is top 80 percent: call
        elif handPercent <= .80:
            return Action.CALL
        # else fold
        return Action.FOLD
