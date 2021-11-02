from environment.Constants import Action
from environment.FixedLimitPoker import FixedLimitPoker
from bots import UnitTesterBot, EmptyBot
from unittest import TestCase


class TestActions(TestCase):

    def testFold(self):
        env = FixedLimitPoker([UnitTesterBot(actions=[Action.FOLD]), EmptyBot()])
        actionSpace,_,reward,isDone = env.reset()
        self.assertListEqual([], actionSpace)
        self.assertTrue(isDone)
        self.assertEqual(5, reward)

    def testCallCheck(self):
        env = FixedLimitPoker([UnitTesterBot(actions=[Action.CALL, Action.CHECK]), EmptyBot()])
        actionSpace,obs,reward,isDone = env.reset()
        self.assertListEqual([Action.CHECK, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(20, obs.totalPot)

        actionSpace,obs,reward,isDone = env.step(Action.CHECK)
        self.assertListEqual([Action.CHECK, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(3, len(obs.boardCards))
        self.assertEqual(20, obs.totalPot)

    def testCallRaiseCall(self):
        env = FixedLimitPoker([UnitTesterBot(actions=[Action.CALL, Action.CALL, Action.CHECK]), EmptyBot()])
        actionSpace,obs,reward,isDone = env.reset()
        self.assertListEqual([Action.CHECK, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(20, obs.totalPot)

        actionSpace,obs,reward,isDone = env.step(Action.RAISE)
        self.assertListEqual([Action.CHECK, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(3, len(obs.boardCards))
        self.assertEqual(40, obs.totalPot)

    def testCallRaiseRaiseCall(self):
        env = FixedLimitPoker([UnitTesterBot(actions=[Action.CALL, Action.RAISE, Action.CHECK]), EmptyBot()])
        actionSpace,obs,reward,isDone = env.reset()
        self.assertListEqual([Action.CHECK, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(20, obs.totalPot)

        actionSpace,obs,reward,isDone = env.step(Action.RAISE)
        self.assertListEqual([Action.FOLD, Action.CALL, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(50, obs.totalPot)

        actionSpace,obs,reward,isDone = env.step(Action.CALL)
        self.assertListEqual([Action.CHECK, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(3, len(obs.boardCards))
        self.assertEqual(60, obs.totalPot)

    def test4RaiseIsMax(self):
        env = FixedLimitPoker([UnitTesterBot(actions=[Action.CALL, Action.RAISE, Action.RAISE]), EmptyBot()])

        actionSpace,obs,reward,isDone = env.reset()
        self.assertListEqual([Action.CHECK, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(20, obs.totalPot)

        actionSpace,obs,reward,isDone = env.step(Action.RAISE)
        self.assertListEqual([Action.FOLD, Action.CALL, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(50, obs.totalPot)

        actionSpace,obs,reward,isDone = env.step(Action.RAISE)
        self.assertListEqual([Action.FOLD, Action.CALL], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(90, obs.totalPot)

        #try to raise a 5th time should result in call
        actionSpace,obs,reward,isDone = env.step(Action.RAISE)
        self.assertListEqual([Action.CHECK, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(100, obs.totalPot)

    def testFoldWhenCheckIsAllowed(self):
        env = FixedLimitPoker([UnitTesterBot(actions=[Action.CALL, Action.CHECK]), EmptyBot()])
        actionSpace,obs,reward,isDone = env.reset(stackedDeck=["As","Ah",  "2c","3c",  "Ad","Ac","Kc","Ks","Ts"])
        self.assertListEqual([Action.CHECK, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(20, obs.totalPot)

        actionSpace,obs,reward,isDone = env.step(Action.FOLD)
        self.assertListEqual([Action.CHECK, Action.RAISE], actionSpace)
        self.assertFalse(isDone)
        self.assertEqual(0, reward)
        self.assertEqual(3, len(obs.boardCards))
        self.assertEqual(20, obs.totalPot)
