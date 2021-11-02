import itertools
import pandas as pd
from bots import PercentBot
from bots.CounterBot import CounterBot
from bots.TemplateBot import TemplateBot
from environment.FixedLimitPoker import FixedLimitPoker
from environment.observers.LoggingObserver import LoggingObserver


def debug():
    observers = [LoggingObserver()]
    env = FixedLimitPoker(
        [PercentBot(), TemplateBot()], observers=observers)
    env.reset()
    env.reset(rotatePlayers=True)

def benchmark():
    bots = [CounterBot(),PercentBot()]#,TemplateBot()]
    combinations = list(itertools.combinations(bots, 2))
    roundsPerPair = 1000
    cols = [x.name for x in bots]
    stats = pd.DataFrame(0, columns=cols, index=cols + ["sum", "pr. round"])
    for c in combinations:
        room = FixedLimitPoker(c)
        for _ in range(roundsPerPair):
            room.reset(rotatePlayers=True)
            p1 = room.players[0]
            p2 = room.players[1]
            stats[p1.bot.name][p2.bot.name] += p1.reward
            stats[p1.bot.name]["sum"] += p1.reward
            stats[p2.bot.name][p1.bot.name] += p2.reward
            stats[p2.bot.name]["sum"] += p2.reward
    for bot in bots:
        stats[bot.name]["pr. round"] = stats[bot.name]["sum"] / (roundsPerPair*(len(bots)-1))
    print(stats)

#benchmark()
debug()