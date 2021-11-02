from typing import Sequence

from environment.Constants import Stage
from environment.PlayerObservation import PlayerObservation


class Observation:
    boardCards: Sequence[str] # community cards on the board. These cards are shared with your opponent
    stage: Stage # current stage of the hand. (PREFLOP, FLOP, TURN, RIVER)
    totalPot: int # total chips in the pot
    stagePot: int # chips wagered in the current stage
    players: Sequence[PlayerObservation] # list of players (you and your opponent) 
    myPosition: int # your position in the player list (0 or 1)
    myHand: Sequence[str] # my cards (['As','Ah'] or ['3h','9d'] or ['Ts', Jh'] or ...)

    def __init__(self) -> None:
        self.boardCards = []
        self.players = []
        self.stage = Stage.PREFLOP
        self.totalPot = 0
        self.stagePot = 0
        self.myPosition = 0
        self.myHand = []
