"""Simple wait-for-db script used by the container entrypoint.
It tries to connect to the database specified in DATABASE_URL env var (Postgres),
or returns immediately if no DATABASE_URL (using sqlite file).
"""
import os
import time
import sys

DATABASE_URL = os.environ.get('DATABASE_URL')

def wait_postgres(url, retries=20, delay=3):
    import dj_database_url
    import psycopg2
    cfg = dj_database_url.parse(url)
    user = cfg.get('USER') or cfg.get('user')
    password = cfg.get('PASSWORD') or cfg.get('password')
    host = cfg.get('HOST') or cfg.get('host')
    port = cfg.get('PORT') or cfg.get('port')
    dbname = cfg.get('NAME') or cfg.get('name')
    dsn = f"host={host} port={port} dbname={dbname} user={user} password={password}"
    attempt = 0
    while attempt < retries:
        try:
            psycopg2.connect(dsn)
            print('Database reachable')
            return 0
        except Exception as e:
            attempt += 1
            print(f'Waiting for Postgres... ({attempt}/{retries})', file=sys.stderr)
            time.sleep(delay)
    print('Could not connect to Postgres after retries', file=sys.stderr)
    return 1

if __name__ == '__main__':
    if DATABASE_URL and DATABASE_URL.startswith('postgres'):
        sys.exit(wait_postgres(DATABASE_URL))
    else:
        # If using sqlite or no DATABASE_URL specified, nothing to wait for.
        print('No external DATABASE_URL detected; skipping wait')
        sys.exit(0)
