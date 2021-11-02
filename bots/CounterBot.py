"""This bot tries to counter the actions of the opponent"""
import itertools
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action
from environment.Observation import Observation


class CounterBot(BotInterface):
    """
    CounterBot plays poker by only trying to play the opponent.

    It tries to exploit the information other bots give, 
    meaning that when they check or call, they maybe don't have any good cards.

    It then raises trying to get the other bot to fold, 
    or at least get them to bet a lot of money with their bad cards.

    It might not have any good cards itself, so it can go terribly wrong ...
    """

    def __init__(self, name="counter"):
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        # get opponent's last action this stage, so we can counter it
        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        # Get the last action the opponent have done
        last_action = opponent_actions_this_round[-1] if len(
            opponent_actions_this_round) > 0 else None

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
        return Action.FOLD
