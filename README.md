Getting started
===============
1. Fork this repository on Github and continue from there.

Setup
=====

To setup your environment do the following:
1. Download python3 for your os
2. Create a virtual environment: `python -m venv venv`
3. Use that environment: `venv\Scripts\activate`
4. Install the project dependencies: `pip install -r requirements.txt`

Developing your bot
===================
1. In the `bots` folder, create a file with the name of your bot i.e. `ChallengerBot.py`
2. Copy the contents from `EmptyBot.py` into it




Todo liste
==========
- [X] Tilføj oberserver pattern - Troels
  - [X] Tilføj console observer - Troels
  - [X] Tilføj Websocket observer - Troels
- [X] Tilføj tests - Bovle
- [ ] Lav UI - Harder
  - [x]  slider for hænder i kamp
  - [ ]  vis action som skrift på avatar
  - [ ]  vis score for kamp
  - [ ]  vis hånd typer ved showdown
  - [ ]  vis chips vundet ved showdown
  - [ ]  fix state 0
  - [x]  slider ændringer korrekt
- [X] Lav UI Data
  - [X] JSON kamp data 
- [X] Hjælp til bot udvikling
  - [X] preflop hånd rang 
  - [X] postflop hånd rang
  - [X] Bedre bot eksempler
- [X] Håndter multiple kampe samtidig
  - [X] Spil N bots mod hinanden alle mod alle
  - [X] Gem resultat som matchup tabel
- [X] Fejlhåndtering
  - [X] Hvis de crasher
  - [X] Hvis de tager for lang tid (1 sekund?)
- [X] Reimplment scoreboard using Google docs
  - [X] Gather results (in observer?) 
  - [X] Upload raw data to Google sheets
  - [X] Make Google Sheet that displays data in a pretty way
- [ ] Refactor Call and Check into CALL_CHECK
- [ ] Check/fold
- [ ] Forklar handValue utils.
- [ ] Template bot som de kan starte med (tom implementation)
- [ ] Downgrade bots
- [ ] Make a raise loop cause a check/call rather than fold

Nice to have:

- [X] løbende turneringer
  - [X] GitHub gist
  - [X] GitHub repo





Challenge:
 - Much faster (10x) with pypy3 (https://www.pypy.org/download.html)


Sort dependencies:
 - `isort -l 120 bots environment utils main.py read_results.py challenge.py`
 
