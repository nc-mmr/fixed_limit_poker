"""unit test player"""
from typing import List, Sequence

from bots.BotInterface import BotInterface
from environment import Constants
from environment.Observation import Observation


class UnitTesterBot(BotInterface):

    actions: List[Constants.Action]
    idx: int

    def __init__(self, name="tester", actions: List[Constants.Action] = []):
        super().__init__(name=name)
        self.actions = actions
        self.idx = 0

    def act(self, action_space: Sequence[Constants.Action], observation: Observation) -> Constants.Action:
        self.idx += 1
        return self.actions[self.idx - 1]
