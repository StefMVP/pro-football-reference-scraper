from typing import List

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

from Player import Player
from Position import Position
from Config import Config


def get_all_players(positions: List[Position], year: int):
    players = []
    r = requests.get(Config.base_url + '/years/' + str(year) + '/fantasy.htm')
    soup = BeautifulSoup(r.content, 'html.parser')
    parsed_table = soup.find_all('table')[0]

    for currCount, row in enumerate(parsed_table.find_all('tr')[2:]):
        try:
            if currCount == Config.maxPlayers:
                break

            dat = row.find('td', attrs={'data-stat': 'player'})
            if not dat:
                continue
            name = dat.a.get_text()
            stub = dat.a.get('href')
            stub = stub[:-4]
            pos = row.find('td', attrs={'data-stat': 'fantasy_pos'}).get_text()
            if positions and Position.str_to_enum(pos) not in positions:
                continue
            players.append(Player(name, pos, stub))
        except Exception as e:
            print(e)

    return players


def get_fantasy_data(players: List[Player], year: int):
    df = []
    for player in players:
        print("Start Player.py ", player.Name)
        try:
            tdf = pd.read_html(Config.base_url + player.UrlStub + '/fantasy/' + str(year))[0]

            tdf = tdf.rename(columns={tdf.columns[4][-1]: 'Away'})
            tdf = tdf.rename(lambda x: '' if str(x).startswith("Unnamed") else str(x), axis=1)

            tdf.columns = [' '.join(col).strip() for col in tdf.columns.values]

            tdf['Away'] = [1 if r == '@' else 0 for r in tdf['Away']]

            tdf = tdf.query('Date != "Total"')

            tdf['Name'] = player.Name
            tdf['Position'] = player.Position
            tdf['Season'] = year

            tdf = tdf.drop(columns={'Rk'})

            df.append(tdf)
            print("End Player.py ", player.Name)

        except Exception as e:
            print("ERROR: ", e)

    return df


for year in Config.years:
    players = get_all_players(Config.positions, year)
    fantasy_data = get_fantasy_data(players, year)

    if len(fantasy_data) > 0:
        fantasy_data = pd.concat(fantasy_data)
        fantasy_data.to_csv('data/fantasy2021' + str(time.time()) + '.csv')


