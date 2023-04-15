"""
This is the continuation of something great
Authors: Guan and Taylor
Date: 15 April 2023
"""

import pandas as pd
import psycopg2
from riotwatcher import LolWatcher, ApiError
import os
from dotenv import load_dotenv

load_dotenv()

# global variables
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
cloudinfo = os.getenv('DB_CLOUD')
api_key = os.getenv('RIOT_API')
connection_string = f"postgresql://{user}:{password}{cloudinfo}"
conn = psycopg2.connect(connection_string)
watcher = LolWatcher(api_key)


def fetch(conn, table_name):
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name};"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()


fetch(conn, "matches")
fetch(conn, "timelines")
