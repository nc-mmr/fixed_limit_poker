from unittest import TestCase
from environment.Constants import Action, Stage
from environment.Observation import Observation
from environment.PlayerObservation import PlayerObservation


class TestObservation(TestCase):
    def test_get_observation(self):
        obs = Observation()
        me = PlayerObservation()
        opponent = PlayerObservation()
        me.name = "me"
        opponent.name = "opponent"
        obs.players = [
            me, opponent
        ]
        obs.myPosition = 0
        self.assertEqual(obs.get_opponent_observation(), opponent)
        self.assertEqual(obs.get_own_observation(), me)

    def test_get_history_current_stage(self):
        obs = Observation()
        me = PlayerObservation()
        opponent = PlayerObservation()
        me.name = "me"
        opponent.name = "opponent"
        opponent.history[Stage.FLOP] = [Action.RAISE, Action.RAISE]
        me.history[Stage.FLOP] = [Action.RAISE, Action.CALL]
        obs.players = [
            me, opponent
        ]
        obs.myPosition = 0
        obs.stage = Stage.FLOP
        self.assertEqual(obs.get_opponent_history_current_stage(), [
                         Action.RAISE, Action.RAISE])
        self.assertEqual(obs.get_own_history_current_stage(), [
                         Action.RAISE, Action.CALL])
