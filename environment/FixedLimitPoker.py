from copy import deepcopy
import time
from typing import List, Tuple

from bots.BotInterface import BotInterface
from environment.Constants import Action, Stage
from environment.Deck import Deck
from environment.Observation import Observation
from environment.observers import Observer, OmnipotentObservation
from environment.Player import Player
from environment.PlayerObservation import PlayerObservation
from utils.deuces.card import Card
from utils.deuces.evaluator import Evaluator


class FixedLimitPoker:
    boardCards: List[str]
    stage: Stage
    totalPot: int
    stagePot: int
    players: List[Player]
    activePlayerQueue: List[int]
    numPlayers: int
    smallBlind: int
    bigBlind: int
    stackSize: int
    actionSpace: List[Action]
    deck: Deck
    raiseCount: int
    evaluator: Evaluator
    observers: List[Observer]

    def __init__(self, players: List[BotInterface], smallBlind=5, bigBlind=10, stackSize = 1000, observers=[]):
        self.players = [Player(player) for player in players]
        self.numPlayers = len(self.players)
        self.smallBlind = smallBlind
        self.bigBlind = bigBlind
        self.stackSize = stackSize
        self.evaluator = Evaluator()
        self.observers = observers

    def reset(self, rotatePlayers=False, stackedDeck:List[str]=[]) -> Tuple[List[Action],Observation,int,bool]:    
        self.boardCards = []
        self.activePlayerQueue = []
        self.stage = Stage.PREFLOP
        self.totalPot = 0
        self.stagePot = 0
        self.raiseCount = 0
        self.actionSpace = [Action.FOLD, Action.CALL, Action.RAISE]
        if rotatePlayers:
            self.rotatePlayers()
        for i in range(self.numPlayers):
            self.players[i].reset(stack=self.stackSize, position=i)
            self.activePlayerQueue.append(i)
        self.postBlinds()
        self.deck = Deck()
        if len(stackedDeck) > 0:
            self.deck.cards = stackedDeck
        self.dealHands()
        self.observeNewGame()
        if self.getCurrentPlayer().isAutoPlayer():
            action = self.getAutoPlayerMove()
            result = self.step(action)
            return result
        return (self.actionSpace, self.getObservation(), 0, False)
    
    def rotatePlayers(self) -> None:
        self.players.append(self.players.pop(0))

    def step(self, action:Action) -> Tuple[List[Action],Observation,int,bool] :
        if not action in self.actionSpace:
            action = self.getNearestAllowedAction(action)
        self.executeStep(action)
        self.nextPlayer(action)
        
        if self.isRoundOver():
            
            if len(self.activePlayerQueue) == 1:
                self.stage = Stage.END_HIDDEN
            else:
                self.stage = Stage(self.stage.value+1)
            self.newRound()
            self.observeNewRound()
        
        if self.stage == Stage.END_HIDDEN or self.stage == Stage.SHOWDOWN:
            winnerPositions = self.getWinnerPositions()
            self.giveRewards(winnerPositions)
            self.observeGameOver(winnerPositions)
            for player in self.players:
                if not player.isAutoPlayer():
                    return ([], self.getObservation(), player.reward, True)
            return ([], None, 0, True)
            
        self.updateActionSpace()
        if self.getCurrentPlayer().isAutoPlayer():
            move = self.getAutoPlayerMove()
            return self.step(move)
        else:
            return (self.actionSpace, self.getObservation(), 0, False)

    def giveRewards(self, winnerPositions: List[int]):
        for player in self.players:
            player.win = player.position in winnerPositions
            player.reward = self.getReward(player, player.win, len(winnerPositions))

    def getReward(self, player:Player, win:bool, numWinners:int = 1):
        wagered = (self.stackSize - player.stack)
        if win:
            return int(self.totalPot / numWinners) - wagered
        else:
            return wagered * -1

    def getWinnerPositions(self) -> List[int]:
        winnerVal = 10000
        winners = []

        # Don't calculate anything if there's only one player left
        if len(self.activePlayerQueue) == 1:
            return list(self.activePlayerQueue)

        board = [Card.new(c) for c in self.boardCards]
        for i in self.activePlayerQueue:
            hand = [Card.new(c) for c in self.players[i].hand]
            val, _ = self.evaluator.evaluate(board, hand)
            if val < winnerVal:
                winnerVal = val
                winners = [i]
            elif val == winnerVal:
                winners.append(i)
        return winners
        

    def newRound(self) -> None:
        self.activePlayerQueue = sorted(self.activePlayerQueue)
        self.stagePot = 0
        self.raiseCount = 0
        for i in self.activePlayerQueue:
            self.players[i].contribution = 0
        if self.stage == Stage.FLOP:
            self.boardCards = self.deck.drawMultiple(3)
        elif self.stage.value <= Stage.RIVER.value:
            self.boardCards.append(self.deck.draw())
        
    def updateActionSpace(self) -> None:
        actions = []
        if self.raiseCount == 0 and (self.stage != Stage.PREFLOP or            # after first round no raisers
            (self.stage == Stage.PREFLOP and self.activePlayerQueue[0] == 1)): # first round all call/fold to big blind
                actions.append(Action.CHECK)
        else:
            actions.append(Action.FOLD)
            if self.getCurrentPlayer().stack >= self.getCallAmount():
                actions.append(Action.CALL)

        if self.raiseCount != 4 and self.getCurrentPlayer().stack > self.getCallAmount():
            actions.append(Action.RAISE)
            
        self.actionSpace = actions


    def nextPlayer(self, action:Action) -> None:
        if action == Action.FOLD:
            self.activePlayerQueue.pop(0)
        else:
            self.activePlayerQueue.append(self.activePlayerQueue.pop(0))
            

    def executeStep(self, action:Action) -> None:
        currentPlayer = self.getCurrentPlayer()
        currentPlayer.history[self.stage].append(action)
        if action == Action.CHECK:
            pass
        elif action == Action.FOLD:
            currentPlayer.active = False
        elif action == Action.CALL:
            amount = self.getCallAmount()
            self.postAmount(currentPlayer, amount)
        elif action == Action.RAISE:
            self.raiseCount += 1
            amount = min(self.getCallAmount() + self.getRaiseAmount(), currentPlayer.stack)
            self.postAmount(currentPlayer, amount)
        self.observePlayerAction(currentPlayer, action)

    def isRoundOver(self):
        if len(self.activePlayerQueue) == 1:
            return True
        if all([self.players[i].stack == 0 for i in self.activePlayerQueue]):
            return True
        if self.raiseCount > 0 and self.equalContribution():
            return True
        if self.allChecked():
            return True
        return False

    def allChecked(self) -> bool:
        bigBlindHistory = self.players[1].history[self.stage]
        if self.stage == Stage.PREFLOP and len(bigBlindHistory) > 0 and bigBlindHistory[0] == Action.CHECK: #preflop and bigblind checked
            return True
        for player in self.players:
            if player.active:
                hist = player.history[self.stage]
                if len(hist) == 0 or hist[-1] != Action.CHECK:
                    return False

        return True

    def equalContribution(self) -> bool:
        contributions = []
        for player in self.players:
            if player.active:
                contributions.append(player.contribution)
        return len(set(contributions)) == 1
        
    def getNearestAllowedAction(self, action:Action) -> Action:
        if action == Action.RAISE:
            return Action.CALL
        elif action == Action.CALL or action == Action.FOLD:
            return Action.CHECK
        else:
            return Action.FOLD

    def getAutoPlayerMove(self) -> Action:
        try:
            startTime = time.time()
            move = self.getCurrentPlayer().bot.act(self.actionSpace, self.getObservation())
            actTime = time.time() - startTime
            if not __debug__ and actTime >= 1:
                move = Action.FOLD
                print(f"Bot: '{self.getCurrentPlayer().bot.name}' took too long ({actTime}) to return. Folding on their behalf.")
        except Exception as ex:
            move = Action.FOLD
            print(f"Bot: '{self.getCurrentPlayer().bot.name}' caused an exception!!! Folding on their behalf.")
            print(ex)
        return move

    def getObservation(self) -> Observation:
        obs = Observation()
        obs.stage = self.stage
        obs.boardCards = list(self.boardCards)
        obs.myHand = list(self.getCurrentPlayer().hand)
        obs.myPosition = self.activePlayerQueue[0]
        obs.stagePot = self.stagePot
        obs.totalPot = self.totalPot
        obs.players = [self.getPlayerObs(player) for player in self.players]
        return obs

    def getPlayerObs(self, player: Player) -> PlayerObservation:
        playerObs = PlayerObservation()
        playerObs.stack = player.stack
        playerObs.active = player.active
        playerObs.contribution = player.contribution
        playerObs.name = player.bot.name
        playerObs.position = player.position
        playerObs.history =  deepcopy(player.history)
        playerObs.reward = player.reward
        playerObs.win = player.win
        return playerObs

        
    def getCurrentPlayer(self) -> Player:
        return self.players[self.activePlayerQueue[0]]

    def dealHands(self) -> None:
        for player in self.players:
            player.hand = self.deck.drawMultiple(2)

    def getCallAmount(self) -> int:
        maxContribution = max(self.players, key=lambda p: p.contribution).contribution
        return maxContribution - self.getCurrentPlayer().contribution

    def getRaiseAmount(self) -> int:
        if self.stage == Stage.PREFLOP or self.stage == Stage.FLOP:
            return self.bigBlind
        else:
            return self.bigBlind * 2

    def postBlinds(self) -> None:
        playerSmallBlind = self.players[self.activePlayerQueue[0]]
        self.postAmount(playerSmallBlind, self.smallBlind)
        self.activePlayerQueue.append(self.activePlayerQueue.pop(0))

        playerBigBlind = self.players[self.activePlayerQueue[0]]
        self.postAmount(playerBigBlind, self.bigBlind)
        self.activePlayerQueue.append(self.activePlayerQueue.pop(0))
        
    def postAmount(self, player:Player, amount:int) -> None:
        player.postAmount(amount)
        self.stagePot += amount
        self.totalPot += amount

    def observeNewGame(self):
        # Don't do any work if no observers exist
        if not self.observers:
            return

        obs = self.getOmnipotentObservation()

        for observer in self.observers:
            observer.LogNewGame(obs)
            
    def observeNewRound(self):
        # Don't do any work if no observers exist
        if not self.observers:
            return

        obs = self.getOmnipotentObservation()

        for observer in self.observers:
            observer.LogNewRound(obs)

    def observePlayerAction(self, player: Player, action: Action):
        # Don't do any work if no observers exist
        if not self.observers:
            return

        obs = self.getOmnipotentObservation()

        for observer in self.observers:
            observer.LogPlayerAction(obs, player, action)

    def observeGameOver(self, winnerPositions: List[int]):
        # Don't do any work if no observers exist
        if not self.observers:
            return

        obs = self.getOmnipotentObservation()

        for observer in self.observers:
            observer.LogGameOver(obs)

    def getOmnipotentObservation(self):
        omniObservation = OmnipotentObservation()
        omniObservation.stage = self.stage
        omniObservation.boardCards = list(self.boardCards)
        omniObservation.stagePot = self.stagePot
        omniObservation.totalPot = self.totalPot
        omniObservation.players = list([self.getPlayerObs(player) for player in self.players])
        omniObservation.hands = { player.bot.name: player.hand for player in self.players }
        return omniObservation
