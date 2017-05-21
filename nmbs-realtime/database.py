import urlparse

import psycopg2


def get_connection(connection_string):
    result = urlparse.urlparse(connection_string)
    conn = psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    return conn
