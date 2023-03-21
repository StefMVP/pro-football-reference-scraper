# Script Overview

This is a proof-of-concept script that was designed to retrieve player data from https://www.pro-football-reference.com. However, due to the subsequent implementation of rate limiting and bot detection mechanisms, the script is no longer functional in its original form.

## Configuration

To configure the script, follow these steps:

1. Update `Config.py`:
   1. `maxPlayers`: Maximum number of players to scrape at once. Use -1 for infinite.
   2. `maxGamesDebug`: Maximum number of games to scrape at once. Use -1 for infinite.
   3. `years`: Array of years to fetch data for (example: `[2021, 2022]`).
   4. `positions`: Array of positions to fetch data for (example: `[Position.RB]`).
   5. `base_url`: Base URL for pro-football-reference that will be used as a prefix for the URL builder to append to.
   6. `sleep_time`: Wait time in between each call.

## Usage
1) Set up your virtual environment and install the necessary packages.
2) Run `python main.py`
3) Check the `data` folder for a CSV file that contains the retrieved data. The file should be named `fantasy_2021_16794187463595674.csv`.