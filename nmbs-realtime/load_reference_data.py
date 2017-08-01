import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))

import tempfile
import urllib
import zipfile
import pandas as pd
import time
from sqlalchemy import create_engine
import psycopg2


def persist_reference_tables(url, connection_string):
    clean_reference_tables(connection_string, 'sql/feed_ddl.sql')
    path = tempfile.gettempdir() + '/feed.zip'
    urllib.urlretrieve(url, path)
    zip = zipfile.ZipFile(path)
    files = [f for f in zip.namelist() if f.endswith('.txt')]
    for file in files:
        with zip.open(file) as f:
            table_name = file.replace(".txt", "")
            persist_reference_table_from_csv(connection_string, table_name, f)


def clean_reference_tables(connection_string, feed_ddl_path):
    print "dropping tables..."
    with psycopg2.connect(connection_string) as conn:
        cur = conn.cursor()
        with open(feed_ddl_path, 'r') as f:
            statements = f.read().split(";")
            for statement in statements:
                if len(statement) > 1:
                    cur.execute(statement)
        conn.commit()
    print "done"


def persist_reference_table(connection_string, table_name, file):
    conn = None
    try:
        start = time.time()
        print "persisting %s..." % table_name
        df = pd.DataFrame.from_csv(file)
        engine = create_engine(connection_string)
        if table_name == 'calendar_dates':
            df['date'] = pd.to_datetime(df['date'].astype(str), format="%Y%m%d")
        df.to_sql(table_name, engine, if_exists='replace')
        print "total seconds: %d" % (time.time() - start)
    finally:
        if conn is not None:
            conn.close()


def persist_reference_table_from_csv(connection_string, table_name, file):
    conn = None
    try:
        start = time.time()
        print "persisting %s..." % table_name
        df = pd.DataFrame.from_csv(file)
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        if table_name == 'calendar_dates':
            df['date'] = pd.to_datetime(df['date'].astype(str), format="%Y%m%d")
        tempdir = tempfile.gettempdir() + "/feed_csv/"
        csv_name = tempdir + table_name + "_pandas.csv"
        df.to_csv(csv_name, header=False)
        with open(csv_name, 'r') as f:
            cur.copy_from(f, table_name, sep=',', null='')
        conn.commit()
        # df.to_sql(table_name, engine, if_exists='replace')
        print "total seconds: %d" % (time.time() - start)
    finally:
        if conn is not None:
            conn.close()


def lambda_handler(event, context):
    feed_url = os.environ['nmbs_feed_url']
    connection_string = os.environ['nmbs_connection_string']
    persist_reference_tables(feed_url, connection_string)


def run_local(config_path):
    from config import Config
    config = Config(config_path)
    persist_reference_tables(config.feed_url, config.connection_string_local)


def run(config_path):
    from config import Config
    config = Config(config_path)
    persist_reference_tables(config.feed_url, config.connection_string)

# run_local('config.json')
