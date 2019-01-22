import os

import psycopg2

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE users (
        user_id uuid PRIMARY KEY,
        last_seen timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
        created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
    );
""")

cur.execute("""
    CREATE TABLE things (
        user_id uuid REFERENCES users (user_id),
        has_things boolean DEFAULT False
    );
""")

conn.commit()
conn.close()
