"""stalls and waits for x seconds before returning"""
from typing import Sequence

from bots.BotInterface import BotInterface
from environment import Constants
from environment.Observation import Observation

import time


class StallBot(BotInterface):
    stallTime = 1

    def __init__(self, name="stallbot", stallTime=1):
        super().__init__(name=name)
        self.stallTime = stallTime

    def act(self, action_space: Sequence[Constants.Action], observation: Observation) -> Constants.Action:
        
        time.sleep(self.stallTime)
        return Constants.Action.RAISE
