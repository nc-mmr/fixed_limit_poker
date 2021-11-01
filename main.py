from bots import PercentBot
from bots.CounterBot import CounterBot
from bots.TroelsBot import TroelsBot
from environment.FixedLimitPoker import FixedLimitPoker
from environment.observers.LoggingObserver import LoggingObserver


def main():
    observers = [LoggingObserver()]
    env = FixedLimitPoker(
        [PercentBot(), TroelsBot()], observers=observers)
    env.reset()
    # env.reset(rotatePlayers=True)
    # env.reset(rotatePlayers=True)
    # env.reset(rotatePlayers=True)
    # env.reset(rotatePlayers=True)


main()
