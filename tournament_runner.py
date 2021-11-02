import glob
import importlib
import re
import urllib.request
from datetime import datetime
from os import makedirs, sep
from os.path import dirname, exists, join
from time import sleep

import gspread
from gspread_pandas import Spread, Client
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

import challenge

NOW = datetime.now()
PRETTY_TIMESTAMP = f"{NOW.year}{NOW.month}{NOW.day}-{NOW.hour}{NOW.minute}{NOW.second}"
PATH_TO_BOTS_RELATIVE = f"results\\{PRETTY_TIMESTAMP}\\bots"
PATH_TO_BOTS = join(dirname(__file__), PATH_TO_BOTS_RELATIVE)

BOT_LOCATIONS = [
    "https://raw.githubusercontent.com/bovle/fixed_limit_poker/main/bots/TemplateBot.py",
    "https://raw.githubusercontent.com/bovle/fixed_limit_poker/main/bots/TemplateBot.py",
    "https://raw.githubusercontent.com/bovle/fixed_limit_poker/main/bots/TemplateBot.py",
    "https://gist.githubusercontent.com/VirtualSatai/3b329b8224cdb91ac67da296d630edba/raw/GistBot2.py",
    "https://gist.githubusercontent.com/VirtualSatai/3b329b8224cdb91ac67da296d630edba/raw/GistBot2.py"
]


def download_bots():
    # make folders
    makedirs(PATH_TO_BOTS, 0o666)

    # download bots
    for b in BOT_LOCATIONS:
        try:
            with urllib.request.urlopen(b) as bot:
                bot_source = bot.read().decode('utf-8')

                # Write snapshot of bot to file:
                bot_name = b.split("/")[-1]
                filepath = join(PATH_TO_BOTS, bot_name)
                while exists(filepath):
                    oldpath = filepath
                    filepath = filepath.split(".py")[0] + "_dedup.py"
                    print("Duplicate filename: " +
                          oldpath.split(sep)[-1] + " renaming to " + filepath.split(sep)[-1])
                with open(filepath, 'w') as file:
                    file.write(bot_source)
                print(f"Downloaded bot: {b}")
        except Exception as ex:
            print("Exception while trying to download a bot: " + b)
            print(ex)


def upload_results(res):
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "client_secret_tbk.json", scope)
    client = gspread.authorize(creds)
    spread = Spread('Poker Bot Wars 2.0', client=client,
                    creds=creds, scope=scope)
    # spreadsheet = client.open("Poker Bot Wars 2.0")
    newsheetname = f"res-{PRETTY_TIMESTAMP}"
    spread.df_to_sheet(
        res,
        index=True,
        sheet=newsheetname,
        start="A1"
    )
    main_sheet = spread.find_sheet("Main")
    # Update A1 cell to force update the sheet
    main_sheet.update("A1", "Updating data ...")
    sleep(1.0)
    main_sheet.update("A1", "")


def get_bots():
    bots = []
    # dynamically import them all
    # https://stackoverflow.com/a/1057534
    modules = glob.glob(join(PATH_TO_BOTS, "*.py"))
    regex = re.compile(r"class (\w*?)\(BotInterface\)")
    for m in modules:
        # we need to convert the filepath to a "module" style path like "os.path" rather than "os/path.py".
        # first remove prefix (to make it relative)
        # then replace the seperator with dots
        # then remove the .py extension
        dotted_name = m.replace(
            join(dirname(__file__)) + sep, "").replace(sep, ".").replace(".py", "")
        # import the file as a module
        imp = importlib.import_module(dotted_name, package=__name__)
        class_name = dotted_name.split(".")[-1]
        # get its constructor
        with open(m, "r") as f:
            match = [regex.match(l) for l in f.readlines() if regex.match(l)]
            if len(match) > 0:
                class_name = match[0].group(1)
        model = getattr(imp, class_name)
        # make instance of class
        NClass = model()
        bots.append(NClass)
    return bots


def download_and_get_bots():
    download_bots()
    return get_bots()


def main():
    # Plan:
    # Download all the bots (snapshot) into a folder (in results?) from either github or gist
    bots = download_and_get_bots()

    # run the tournament with them
    challenge.PARTICIPANTS = bots
    # challenge.TIMESTAMP = NOW
    res = challenge.main()

    upload_results(res)


if __name__ == "__main__":
    main()
