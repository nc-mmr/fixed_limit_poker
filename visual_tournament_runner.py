import math
import random
import json
import time
from bots import CounterBot, PercentBot, TemplateBot
from environment.FixedLimitPoker import FixedLimitPoker
from environment.observers.JsonObserver import JsonObserver
from tournament_runner import get_bots, download_and_get_bots

def main():
    handsPerGame = 100
    bots = download_and_get_bots()
    players = {}
    for bot in bots:
        while bot.name in players.keys():
            newName = bot.name + '_1'
            print("bot already in list!")
            print("changed " + bot.name + " to " + newName)
            bot.name = newName
        players[bot.name] = bot

    tournament = Tournament(list(players.keys()))
    
    tournament.generate_bracket('single', False)
    games = []
    for game_id, game_data in tournament.games.items():
        obs = JsonObserver()
        env = FixedLimitPoker([getBotFromPlayer(players, p) for p in game_data.players], observers=[obs])
        for _ in range(handsPerGame):
            env.reset(rotatePlayers=True)
        infoObj, winner = obs.ToSimpleObject(game_id.split('g')[1], game_id.split('g')[0])
        tournament.play_game(game_id, winner)
        games.append(infoObj)
    jsondata = json.dumps(games)
    with open(f"./results/games-{round(time.time())}.json", 'w') as file:
        json.dump(games, file)
        print("Wrote to file ...")
    print()

def getBotFromPlayer(players, player):
    return players[player[0].get('winner') if type(player) is tuple else player]


def getTournamentStage(stageNumber):
    if stageNumber == '1':
        return "finale"
    elif stageNumber == '2':
        return "semifinale"
    elif stageNumber == '3':
        return "kvartfinale"
    elif stageNumber == '4':
        return "ottendedelsfinale"
    elif stageNumber == '5':
        return "sekstendedelsfinale"


def generate_bracket_rec(players):
    games_map = {}
    next_players = []

    assert len(players) > 0

    if len(players) == 1:
        return games_map

    for i in range(int(len(players) / 2)):
        player1_id = i
        player2_id = len(players) - 1 - i

        if players[player2_id] is None:
            next_players.append(players[player1_id])
        else:
            game_id = str(int(math.log(len(players), 2))) + "g" + str(i + 1)
            g = Game((players[player1_id], players[player2_id]), game_id)
            games_map[g.id] = g
            next_players.append((g, "winner"))
    d = {}
    d.update(games_map)
    d.update(generate_bracket_rec(next_players).items())
    return d


# Players in each game will either be string literals
# or tuples that contain a Game and "loser" or "winner"
class Game:
    def __init__(self, players, game_id=None):
        self.players = players
        self.done = False
        self.id = random.getrandbits(24) if game_id is None else game_id

    def __str__(self):
        output = self.id + ": "
        first_raw = self.players[0]
        output += (first_raw[0].get(first_raw[1]) if type(self.players[0]) is tuple else first_raw) + " vs "
        output += (self.players[1][0].get(self.players[1][1]) if type(self.players[1]) is tuple else self.players[1])
        return output

    def __repr__(self):
        output = str(self)
        output = output + "\nDone: " + \
            str(self.done) + (" | Winner: " + self.winner + " Loser: " + self.loser if self.done else "")
        return output

    def get_raw_players(self):
        return tuple(player[0].get(player[1]) if type(player) is tuple else player for player in self.players)

    def is_ready(self):
        for player in self.players:
            if type(player) is tuple and not player[0].done:
                return False
        return True

    def play_game(self, winning_player):
        # TODO: Deal with fact that this is just the is_ready method again
        for player in self.players:
            if type(player) is tuple and not player[0].done:
                print("ERROR 1: Attempting to start " + self.id + " before " + player[0].id + " is complete")
                return False

        players_raw = tuple(player[0].get(player[1]) if type(player) is tuple else player for player in self.players)
        if winning_player not in players_raw:
            print("ERROR 2: " + winning_player + " not in " + self.id)
            return False

        self.winner = winning_player
        self.loser = players_raw[0] if players_raw[1] == winning_player else players_raw[1]
        self.done = True
        return True

    def get(self, item):
        if not self.done:
            return str(item) + " of " + str(self.id)
        else:
            if item == "winner":
                return self.winner
            elif item == "loser":
                return self.loser
            else:
                return "INVALID"


class Tournament:
    def __init__(self, players):
        self.players = players
        self.player_count = len(players)
        self.games = {}

    def __str__(self):
        output = ""
        for s in self.players:
            output = output + ((s + " ") if s is not None else "")
        output += "\nlog(Size): " + str(self.n_size)
        output += " | underflow: " + str(self.underflow)
        return output

    def __repr__(self):
        return self.__str__()

    def generate_bracket(self, bracket_class, randomize):
        if bracket_class != "single":
            print("Illegal bracket class")
            quit()

        self.n_size = int(math.ceil(math.log(self.player_count, 2)))
        self.underflow = int(math.pow(2, self.n_size) - self.player_count)

        if randomize:
            random.shuffle(self.players)

        for i in range(self.underflow):
            self.players.append(None)

        self.games = generate_bracket_rec(self.players)

    def play_game(self, game_id, game_winner):
        if game_id not in self.games:
            print("ERROR 3: Illegal Game ID " + game_id)
            return False

        if self.games[game_id].done:
            print("ERROR 4: Game aready complete " + game_id)
            return False

        return self.games[game_id].play_game(game_winner)

main()