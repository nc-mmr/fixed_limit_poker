"""Fold player"""
from typing import Sequence

from bots.BotInterface import BotInterface
from environment import Action, Observation


class FoldBot(BotInterface):

    def __init__(self, name="foldalot"):
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        return Action.FOLD
