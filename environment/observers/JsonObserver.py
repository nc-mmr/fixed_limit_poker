import json
from typing import Tuple
from environment import Player
from environment.Constants import Action, Stage
from environment.observers.Observer import Observer
from environment.observers.OmnipotentObservation import OmnipotentObservation
from utils.handValue import getHandType

class JsonObserver(Observer):

    res = {}
    currentHand = {}
    currentPlayer1Index = 0
    currentPlayer2Index = 1
    player1Name = ""
    player2Name = ""
    player1Reward = 0
    player2Reward = 0
    raiseCount = 0

    def __init__(self) -> None:
        self.res = {
            "hands": []
        }

    def LogNewGame(self,observation: OmnipotentObservation) -> None:

        if not "player1" in self.res:
            self.player1Name = observation.players[0].name
            self.res["player1"] = {
                "name": observation.players[0].name
            }
        if not "player2" in self.res:
            self.player2Name = observation.players[1].name
            self.res["player2"] = {
                "name": observation.players[1].name
            }
        
        self.raiseCount = 0
        self.currentPlayer1Index = 0 if observation.players[0].name == self.player1Name else 1
        self.currentPlayer2Index = (self.currentPlayer1Index + 1) % 2

        self.currentHand = {
            "player1": {
                "total_reward_before": self.player1Reward,
                "cards": observation.hands[self.player1Name]
            },
            "player2": {
                "total_reward_before": self.player2Reward,
                "cards": observation.hands[self.player2Name]
            },
            "history":[]
        }

        self.currentHand["history"].append({
            "player": "player1" if observation.players[0].name == self.player1Name else "player2",
            "action": "small_blind",
            "stage_contribution": observation.players[0].contribution,
            "stack": observation.players[0].stack
        })
        self.currentHand["history"].append({
            "player": "player1" if observation.players[1].name == self.player1Name else "player2",
            "action": "big_blind",
            "stage_contribution": observation.players[1].contribution,
            "stack": observation.players[1].stack
        })
        

    def LogNewRound(self,observation: OmnipotentObservation) -> None:
        res = {
            "action": observation.stage.name,
            "board_cards": observation.boardCards,
            "pot": observation.totalPot
        }
        if observation.stage == Stage.SHOWDOWN:
            res["player1_hand_type"] = getHandType(observation.hands[self.player1Name], observation.boardCards)[0].name
            res["player2_hand_type"] = getHandType(observation.hands[self.player2Name], observation.boardCards)[0].name
        self.currentHand["history"].append(res)

    def LogPlayerAction(self, observation: OmnipotentObservation, player: Player, action: Action) -> None:
        self.currentHand["history"].append({
            "player": "player1" if player.bot.name == self.player1Name else "player2",
            "action": action.name,
            "stage_contribution": player.contribution,
            "stack": player.stack
        })
        if action == Action.RAISE:
            self.raiseCount = self.raiseCount + 1

    def LogGameOver(self, observation: OmnipotentObservation) -> None:
        self.currentHand["nbr"] = len(self.res["hands"])+1
        self.currentHand["raise_count"] = self.raiseCount
        self.currentHand["abs_reward"] = abs(observation.players[0].reward)
        self.currentHand["player1"]["winner"] = observation.players[self.currentPlayer1Index].win
        self.currentHand["player2"]["winner"] = observation.players[self.currentPlayer2Index].win
        self.res["hands"].append(self.currentHand)
        self.player1Reward += observation.players[self.currentPlayer1Index].reward
        self.player2Reward += observation.players[self.currentPlayer2Index].reward

    def ToSimpleObject(self, gameNbr: str, tournamentStage: str) -> Tuple[str, str]:
        self.res["game_nbr"] = gameNbr
        self.res["tournament_stage"] = tournamentStage
        self.res["player1"]["total_reward"] = self.player1Reward
        self.res["player1"]["winner"] = True if self.player1Reward >= self.player2Reward else False
        self.res["player2"]["total_reward"] = self.player2Reward
        self.res["player2"]["winner"] = True if self.player2Reward >= self.player1Reward else False
        winnerName = self.player1Name if self.player1Reward >= self.player2Reward else self.player2Name
        return self.res, winnerName
