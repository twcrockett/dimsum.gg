"""
This is the beginning of something great
Authors: Guan and Taylor
Date: 2 April 2023
"""

import psycopg2
from riotwatcher import LolWatcher, ApiError
import os
from dotenv import load_dotenv
import time

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
puuid = os.getenv('DimSumKing')
region = "AMERICAS"
matches = watcher.match.matchlist_by_puuid(region=region, puuid=puuid, type='ranked')
print(matches)

def create_tables(conn):
    cursor = conn.cursor()

    matches_table = '''
    CREATE TABLE IF NOT EXISTS matches (
        match_id VARCHAR(255) PRIMARY KEY,
        game_duration INT,
        game_version VARCHAR(255),
        game_mode VARCHAR(255),
        game_type VARCHAR(255),
        map_id INT,
        queue_id INT
    );
    '''

    timelines_table = '''
        CREATE TABLE IF NOT EXISTS timelines (
            match_id VARCHAR(255),
            participant_id INT,
            timestamp BIGINT,
            position_x INT,
            position_y INT,
            level INT,
            total_gold INT,
            current_gold INT,
            xp INT,
            minions_killed INT,
            jungle_minions_killed INT,
            event_type VARCHAR(255),
            PRIMARY KEY (match_id, participant_id, timestamp),
            FOREIGN KEY (match_id) REFERENCES matches(match_id)
        );
        '''

    cursor.execute(matches_table)
    cursor.execute(timelines_table)
    conn.commit()
    cursor.close()


create_tables(conn)


def get_match(region, match_id):
    # get match data
    match_data = watcher.match.by_id(region, match_id)
    print(match_data)

    # rate limit respect
    time.sleep(3)

    # get timeline data
    match_timeline = watcher.match.timeline_by_match(region, match_id)

    return match_data, match_timeline


def insert_match_data(conn, data):
    cursor = conn.cursor()
    sql = '''
    INSERT INTO matches (match_id, game_duration, game_version, game_mode, game_type, map_id, queue_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (match_id) DO NOTHING;
    '''

    values = (
        match_data['metadata']['matchId'],
        match_data['info']['gameDuration'],
        match_data['info']['gameVersion'],
        match_data['info']['gameMode'],
        match_data['info']['gameType'],
        match_data['info']['mapId'],
        match_data['info']['queueId']
    )

    cursor.execute(sql, values)
    conn.commit()
    cursor.close()

# def insert_timeline_data(conn, match_id, match_timeline):
#     cursor = conn.cursor()
#     sql = '''
#     INSERT INTO timelines (match_id, participant_id, timestamp, position_x, position_y, level, total_gold, current_gold, xp, minions_killed, jungle_minions_killed, event_type)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
#     '''
#
#     for frame in match_timeline['info']['frames']:
#         timestamp = frame['timestamp']
#
#         for pid, pdata in frame['participantFrames'].items():
#             values = (
#                 match_id,
#                 pdata['participantId'],
#                 timestamp,
#                 pdata['position']['x'],
#                 pdata['position']['y'],
#                 pdata['level'],
#                 pdata['totalGold'],
#                 pdata['currentGold'],
#                 pdata['xp'],
#                 pdata['minionsKilled'],
#                 pdata['jungleMinionsKilled'],
#                 None  # event_type is None for participantFrames
#             )
#             cursor.execute(sql, values)
#
#         for event in frame['events']:
#             participant_id = event.get('participantId', None)
#             event_type = event['type']
#
#             if participant_id:
#                 position = event.get('position', {'x': None, 'y': None})
#                 values = (
#                     match_id,
#                     participant_id,
#                     timestamp,
#                     position['x'],
#                     position['y'],
#                     None, None, None, None, None, None,  # level, total_gold, current_gold, xp, minions_killed, jungle_minions_killed are None for events
#                     event_type
#                 )
#                 cursor.execute(sql, values)
#
#     conn.commit()
#     cursor.close()

for match_id in matches:
    # get
    match_data, match_timeline = get_match(region, match_id)

    # insert data into database
    insert_match_data(conn, match_data)
    # insert_timeline_data(conn, match_data['metadata']['matchId'], match_timeline)

    # rate limit respect
    time.sleep(3)
