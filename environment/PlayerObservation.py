from typing import Dict, List

from environment.Constants import Action, Stage


class PlayerObservation:
    name: str # name of the player
    stack: int # current stack (money available to bet)
    contribution: int # chips wagered this stage by this player
    position: int # position at the table 
    active: bool # if player has folded = false, else = true
    win: bool # is this player the winner of this hand
    reward: int # how many chips this player has won/lost in this hand
    history: Dict[Stage, List[Action]] # history of actions represented as a list of actions for each stage

    def __init__(self) -> None:
        self.name = ""
        self.stack = 0
        self.contribution = 0
        self.position = -1
        self.active = True
        self.win = False
        self.reward = 0
        self.history = {}
        for stage in Stage:
            self.history[stage] = []
