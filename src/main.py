from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

error = False
url = 'https://www.pro-football-reference.com'
year = 2021
maxp = 200

# grab fantasy players
r = requests.get(url + '/years/' + str(year) + '/fantasy.htm')
soup = BeautifulSoup(r.content, 'html.parser')
parsed_table = soup.find_all('table')[0]

df = []

# first 2 rows are col headers
for i, row in enumerate(parsed_table.find_all('tr')[2:]):
    if i % 10 == 0: print(i, end=' ')
    if i >= maxp:
        print('\nComplete.')
        break

    try:
        dat = row.find('td', attrs={'data-stat': 'player'})
        if not dat:
            continue
        name = dat.a.get_text()
        stub = dat.a.get('href')
        stub = stub[:-4] + '/fantasy/' + str(year)
        pos = row.find('td', attrs={'data-stat': 'fantasy_pos'}).get_text()
        if pos.trim() != "RB":
            continue

        tdf = pd.read_html(url + stub)[0]

        print("Start Player ", name)

        tdf = tdf.rename(columns={tdf.columns[4][-1]: 'Away'})
        tdf = tdf.rename(lambda x: '' if str(x).startswith("Unnamed") else str(x), axis=1)

        tdf.columns = [' '.join(col).strip() for col in tdf.columns.values]

        tdf['Away'] = [1 if r == '@' else 0 for r in tdf['Away']]

        tdf = tdf.query('Date != "Total"')

        # add other info
        tdf['Name'] = name
        tdf['Position'] = pos
        tdf['Season'] = year

        tdf = tdf.drop(columns={'Rk'})

        df.append(tdf)
        print("End Player ", name)
    except Exception as e:
        print("ERROR: ", e)
        #error = True

if error is False:
    df = pd.concat(df)
    df.to_csv('data/fantasy2021' + str(time.time()) + '.csv')