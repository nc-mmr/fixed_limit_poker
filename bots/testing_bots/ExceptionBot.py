"""throws an exception when the river happens"""
from typing import Sequence

from bots.BotInterface import BotInterface
from environment import Constants
from environment.Observation import Observation


class ExceptionBot(BotInterface):
    def __init__(self, name="exceptionBot"):
        super().__init__(name=name)

    def act(self, action_space: Sequence[Constants.Action], observation: Observation) -> Constants.Action:
        raise Exception
