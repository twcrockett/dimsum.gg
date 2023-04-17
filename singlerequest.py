"""
I ONLY WANT ONE PLEASE.
Authors: Guan and Taylor
Date: 2 April 2023
"""

import psycopg2
from riotwatcher import LolWatcher, ApiError
import os
from dotenv import load_dotenv
import time
import json

load_dotenv()

# global variables
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
cloudinfo = os.getenv('DB_CLOUD')
api_key = os.getenv('RIOT_API')
connection_string = f"postgresql://{user}:{password}{cloudinfo}"
conn = psycopg2.connect(connection_string)
watcher = LolWatcher(api_key)

# let's use DimSumKing
puuid = os.getenv('DimSumKing_puuid')
region = "AMERICAS"
matches = watcher.match.matchlist_by_puuid(region=region, puuid=puuid, type='ranked')
match_id = matches[0]


def get_match(region, match_id):
    # get match data
    match_data = watcher.match.by_id(region, match_id)

    # rate limit respect
    time.sleep(3)

    # get timeline data
    match_timeline = watcher.match.timeline_by_match(region, match_id)

    return match_data, match_timeline


match_data, match_timeline = get_match(region, match_id)

# print(type(match_data))
# print(type(match_timeline))

with open('sample_match.json', 'w') as f:
    json.dump(match_data, f)
with open('sample_timeline.json', 'w') as f:
    json.dump(match_timeline, f)
