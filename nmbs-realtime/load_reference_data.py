import os
import tempfile
import urllib
import zipfile
import pandas as pd
import time
from sqlalchemy import create_engine

from config import Config
from nmbsrealtime.database import get_connection


def run(url, connection_string):
    path = tempfile.gettempdir() + '/feed.zip'
    urllib.urlretrieve(url, path)
    zip = zipfile.ZipFile(path)
    files = [f for f in zip.namelist() if f.endswith('.txt')]
    for file in files:
        with zip.open(file) as f:
            table_name = file.replace(".txt", "")
            persist_reference_table(connection_string, table_name, f)


def persist_reference_table(connection_string, table_name, file):
    conn = None
    try:
        start = time.time()
        print "persisting %s..." %table_name
        df = pd.DataFrame.from_csv(file)
        engine = create_engine(connection_string)
        if table_name == 'calendar_dates':
            df['date'] = pd.to_datetime(df['date'].astype(str), format="%Y%m%d")
        df.to_sql(table_name, engine, if_exists='replace')
        print "total seconds: %d" % (time.time() - start)
    finally:
        if conn is not None:
            conn.close()

def lambda_handler(event, context):
    feed_url = os.environ['nmbs_feed_url']
    connection_string = os.environ['nmbs_connection_string']
    run(feed_url, connection_string)

def run_local():
    config = Config()
    run(config.feed_url, config.connection_string_local)


run_local()
