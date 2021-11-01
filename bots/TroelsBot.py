from typing import Dict, Sequence

from bots.BotInterface import BotInterface
from environment.Constants import RANKS, Action, HandType, Stage
from environment.Observation import Observation
from utils.handValue import getHandPercent, getHandType, getHighestSuitCount, getLongestStraight


class TroelsBot(BotInterface):

    def __init__(self, name="TroelsBot"):
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        stage = observation.stage
        if stage == Stage.PREFLOP:
            return self.getNearestAction(self.handlePreFlop(observation), action_space)
        elif stage == Stage.FLOP:
            return self.getNearestAction(self.handleFlop(observation), action_space)
        elif stage == Stage.TURN:
            return self.getNearestAction(self.handleTurn(observation), action_space)
        elif stage == Stage.RIVER:
            return self.getNearestAction(self.handleRiver(observation), action_space)

        # Unexpected!
        return Action.FOLD

    def handlePreFlop(self, observation: Observation) -> Action:
        handPercent, _ = getHandPercent(observation.myHand)
        if handPercent < .80:
            return Action.RAISE
        elif handPercent < .90:
            return Action.CALL
        return Action.FOLD

    def handleFlop(self, observation: Observation) -> Action:
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        if handPercent <= .50:
            return Action.RAISE
        elif handPercent <= .90 or self.getFlushDraw(observation) or self.getStraightDraw(observation):
            return Action.CALL
        return Action.FOLD

    def handleTurn(self, observation: Observation) -> Action:
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        if handPercent <= .50:
            return Action.RAISE
        elif handPercent <= .70 or self.getFlushDraw(observation) or self.getStraightDraw(observation):
            return Action.CALL
        return Action.FOLD

    def handleRiver(self, observation: Observation) -> Action:
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        if handPercent <= .80:
            return Action.RAISE
        elif handPercent <= .90:
            return Action.CALL
        return Action.FOLD

    def getNearestAction(self, action: Action, actionSpace: Sequence[Action]) -> Action:
        while action not in actionSpace:
            if action.value == 0:
                return Action.CHECK
            action = Action(action.value-1)
        return action

    def getFlushDraw(self, observation: Observation):
        count, suit = getHighestSuitCount(
            observation.myHand, observation.boardCards)
        return count == 4

    def getStraightDraw(self, observation: Observation):
        count, lowRank, highRank = getLongestStraight(
            observation.myHand, observation.boardCards)
        return count == 4
