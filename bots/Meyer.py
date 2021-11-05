"""Meyer"""
import random
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action, Stage
from environment.Observation import Observation
from utils.handValue import getHandPercent

# your bot class, rename to match the file name
class Meyer(BotInterface):

    # change the name of your bot here
    def __init__(self, name="Meyer"):
        '''init function'''
        super().__init__(name=name)

    def act(self, action_space:Sequence[Action], observation:Observation) -> Action:
        # use different strategy depending on pre or post flop (before or after community cards are delt)
        stage = observation.stage

        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        last_action = opponent_actions_this_round[-1] if len(
            opponent_actions_this_round) > 0 else None

        if stage == Stage.PREFLOP:
            return self.handlePreFlop(observation, last_action)

        return self.handlePostFlop(observation, last_action)

    def handlePreFlop(self, observation: Observation, last_action) -> Action:
        if last_action is None:
            # opponent didn't do anything yet for us to counter, just raise
            return Action.RAISE
        elif last_action in [Action.CHECK, Action.CALL]:
            # opponent checked, try to steal the pot with a raise
            return Action.RAISE
        elif last_action == Action.RAISE:
            # opponent raise, probably has good cards so fold
            return Action.FOLD

        # default fold
        return Action.CALL

    def handlePostFlop(self, observation: Observation, last_action) -> Action:
        # get my hand's percent value (how good is the best 5 card hand i can make out of all possible 5 card hands)
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        # if my hand is top 30 percent: raise
        if handPercent <= .30:
            if last_action is None:
                # opponent didn't do anything yet for us to counter, just raise
                return Action.RAISE
            elif last_action in [Action.CHECK, Action.CALL]:
                # opponent checked, try to steal the pot with a raise
                return Action.RAISE
            elif last_action == Action.RAISE:
                # opponent raise, probably has good cards so fold
                return Action.RAISE

            return Action.CALL
        # if my hand is top 80 percent: call
        elif handPercent <= .80:
            if last_action is None:
                # opponent didn't do anything yet for us to counter, just raise
                return Action.CALL
            elif last_action in [Action.CHECK, Action.CALL]:
                # opponent checked, try to steal the pot with a raise
                return Action.RAISE
            elif last_action == Action.RAISE:
                # opponent raise, probably has good cards so fold
                return Action.FOLD

            return Action.FOLD
        # else fold
        return Action.FOLD