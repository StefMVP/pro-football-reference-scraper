from typing import List

from bs4 import BeautifulSoup
from bs4 import Comment
import requests
import pandas as pd
import time
from dateutil.parser import parse

from Game import Game
from Player import Player
from Position import Position
from Config import Config


def get_games(game_data_tds):
    games = []
    for game_data_td in game_data_tds:
        try:
            a_obj = game_data_td.find('a')
            if not a_obj:
                continue
            game_data_stub = a_obj.attrs['href']
            if not game_data_stub:
                continue
            game = get_game_data(game_data_stub)
            games.append(game)
        except Exception as e:
            print("ERROR get_fantasy_data - gamedata: ", e)
    return games


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
            print("ERROR get_all_players: ", e)

    return players


def get_fantasy_data(players: List[Player], year: int):
    df = []
    for player in players:
        print("Start Player ", player.Name)
        try:
            r = requests.get(Config.base_url + player.UrlStub + '/fantasy/' + str(year))
            soup = BeautifulSoup(r.content, 'html.parser')

            game_data_tds = soup.find_all('td', attrs={"data-stat": "game_date"})
            games_data = get_games(game_data_tds)

            parsed_table = soup.find_all('table')[0]

            tdf = pd.read_html(parsed_table.prettify())[0]

            tdf = tdf.rename(columns={tdf.columns[4][-1]: 'Away'})
            tdf = tdf.rename(lambda x: '' if str(x).startswith("Unnamed") else str(x), axis=1)

            tdf.columns = [' '.join(col).strip() for col in tdf.columns.values]

            tdf.loc[:, 'Away'] = [1 if r == '@' else 0 for r in tdf['Away']]

            tdf = tdf.query('Date != "Total"')

            tdf = tdf.assign(Name=player.Name)
            tdf = tdf.assign(Year=year)
            tdf = tdf.drop(columns={'Rk'})

            for index, row in tdf.iterrows():
                rowDate = parse(row['Date'])
                rowDateBefore = tdf.loc[index-1, 'Date'] if index != 0 else ''
                if rowDate and rowDateBefore:
                    tdf.loc[index, 'DaysRest'] = (rowDate - rowDateBefore).days if (rowDate - rowDateBefore) else ''

                for game in games_data:
                    if game.Date == rowDate:
                        tdf.loc[index, 'Date'] = game.Date if game.Date else ''
                        tdf.loc[index, 'StartTime'] = game.StartTime if game.StartTime else ''
                        tdf.loc[index, 'Stadium'] = game.Stadium if game.Stadium else ''
                        tdf.loc[index, 'TimeOfGame'] = game.TimeOfGame if game.TimeOfGame else ''
                        tdf.loc[index, 'Attendance'] = game.Attendance if game.Attendance else ''
                        tdf.loc[index, 'Roof'] = game.Roof if game.Roof else ''
                        tdf.loc[index, 'Surface'] = game.Surface if game.Surface else ''
                        tdf.loc[index, 'Temperature'] = game.Temperature if game.Temperature else ''
                        tdf.loc[index, 'RelativeHumidity'] = game.RelativeHumidity if game.RelativeHumidity else ''
                        tdf.loc[index, 'WindMph'] = game.WindMph if game.WindMph else ''

            df.append(tdf)
            time.sleep(Config.sleep_time)
            print("End Player ", player.Name)

        except Exception as e:
            print("ERROR get_fantasy_data: ", e)
    return df


def get_game_data(game_stub: str):
    print("----Start game ", game_stub)
    try:
        r = requests.get(Config.base_url + game_stub)
        soup = BeautifulSoup(r.content, 'html.parser')
        scorebox = soup.find("div", {"class": "scorebox_meta"})
        date = parse(scorebox.find('div').string) if scorebox.find('div') else None
        startTime = soup.find('strong', string="Start Time").nextSibling if soup.find('strong', string="Start Time") else None
        startTime = startTime.replace(': ','').strip() if startTime else None
        stadium = soup.find('strong', string="Stadium").nextSibling.nextSibling.string if soup.find('strong', string="Stadium") and soup.find('strong', string="Stadium").nextSibling and soup.find('strong', string="Stadium").nextSibling.nextSibling else None
        timeOfGame = soup.find('strong', string="Time of Game").nextSibling if soup.find('strong', string="Time of Game") else None
        timeOfGame = timeOfGame.replace(': ','').strip() if timeOfGame else None
        attendance = soup.find('strong', string="Attendance").nextSibling.nextSibling.string if soup.find('strong', string="Attendance") and soup.find('strong', string="Attendance").nextSibling and soup.find('strong', string="Attendance").nextSibling.nextSibling else None

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        gameInfoComment = None
        for c in comments:
            if "div_game_info" in str(c):
                gameInfoComment = c.extract()
                break

        if gameInfoComment:
            extraSoup = BeautifulSoup(gameInfoComment, 'html.parser')
            gameInfo = extraSoup.find("div", {"id": "div_game_info"})
            gameInfoRows = gameInfo.findAll("tr")
            for gameInfoRow in gameInfoRows:
                th = gameInfoRow.find("th")
                td = gameInfoRow.find("td")
                if not th or not td:
                    continue
                if th.string == "Roof":
                    roof = td.string
                elif th.string == "Surface":
                    surface = td.string
                elif th.string == "Weather":
                    weather = td.string
                    weather = weather.split(', ') if weather else None
                    temperature = weather[0].split(' ')[0] if weather else None
                    relativeHumidity = weather[2].split(' ')[1] if weather else None
                    wind_mph = weather[2].split(' ')[1] if weather else None

        time.sleep(Config.sleep_time)
        print("----End game ", game_stub)

        return Game(date, startTime, stadium, timeOfGame, attendance, roof, surface, temperature, relativeHumidity, wind_mph)

    except Exception as e:
        print("ERROR get_game_data: ", e)


for year in Config.years:
    players = get_all_players(Config.positions, year)
    fantasy_data = get_fantasy_data(players, year)

    if len(fantasy_data) > 0:
        fantasy_data = pd.concat(fantasy_data)
        fantasy_data.to_csv('../data/fantasy_' + str(year) + '_' + str(time.time()).replace('.','') + '.csv')
