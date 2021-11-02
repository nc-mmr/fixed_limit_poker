from typing import List, Sequence

from environment.Constants import Action, Stage
from environment.PlayerObservation import PlayerObservation


class Observation:
    boardCards: Sequence[str]  # community cards on the board. These cards are shared with your opponent
    stage: Stage  # current stage of the hand. (PREFLOP, FLOP, TURN, RIVER)
    totalPot: int  # total chips in the pot
    stagePot: int  # chips wagered in the current stage
    players: Sequence[PlayerObservation]   # list of players (you and your opponent)
    myPosition: int  # your position in the player list (0 or 1)
    myHand: Sequence[str]  # my cards (['As','Ah'] or ['3h','9d'] or ['Ts', Jh'] or ...)

    def __init__(self) -> None:
        self.boardCards = []
        self.players = []
        self.stage = Stage.PREFLOP
        self.totalPot = 0
        self.stagePot = 0
        self.myPosition = 0
        self.myHand = []

    def get_opponent_observation(self) -> PlayerObservation:
        """
        Get the player observation for the opponent.
        """
        return self.players[self.myPosition - 1]

    def get_own_observation(self) -> PlayerObservation:
        """
        Get the player observation for yourself.
        """
        return self.players[self.myPosition]

    def get_opponent_history_current_stage(self) -> List[Action]:
        """
        Get the list of actions the opponent have done in the current stage
        """
        return self.get_opponent_observation().history[self.stage]

    def get_own_history_current_stage(self) -> List[Action]:
        """
        Get the list of actions you have done in the current stage
        """
        return self.get_own_observation().history[self.stage]

