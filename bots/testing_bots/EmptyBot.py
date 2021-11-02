"""empty bot player"""
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action
from environment.Observation import Observation


class EmptyBot(BotInterface):

    def __init__(self, name="empty"):
        super().__init__(name=name, autoPlay=False)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        pass
