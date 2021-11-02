"""Call player"""
from typing import Sequence

from bots.BotInterface import BotInterface
from environment import Constants, Observation


class CallBot(BotInterface):

    def __init__(self, name="callalot"):
        super().__init__(name=name)

    def act(self, action_space: Sequence[Constants.Action], observation: Observation) -> Constants.Action:
        return Constants.Action.CALL
