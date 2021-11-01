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

        return self.getNearestAction(self.handleFlop(observation), action_space)

    def handlePreFlop(self, observation: Observation) -> Action:
        handPercent, _ = getHandPercent(observation.myHand)
        raise_percent = 0.4
        if self.otherPlayerActions(observation, Action.RAISE) >= 1:
            raise_percent *= .5
        if handPercent < raise_percent:
            return Action.RAISE
        elif handPercent < raise_percent * 2:
            return Action.CALL
        return Action.FOLD

    def otherPlayerActions(self, observation, action: Action):
        return observation.players[observation.myPosition - 1].history[observation.stage].count(action)

    def handleFlop(self, observation: Observation) -> Action:
        handPercent, _ = getHandPercent(
            observation.myHand, observation.boardCards)
        if handPercent <= .30:
            return Action.RAISE
        elif handPercent <= .80:
            return Action.CALL
        return Action.FOLD

    def getNearestAction(self, action: Action, actionSpace: Sequence[Action]) -> Action:
        while action not in actionSpace:
            if action.value == 0:
                return Action.CHECK
            action = Action(action.value-1)
        return action
