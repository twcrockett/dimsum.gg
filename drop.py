"""
Goodbye, table
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


def drop_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    conn.commit()
    cursor.close()


drop_table(conn, input("table to drop: "))
