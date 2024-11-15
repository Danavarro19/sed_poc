import os

from psycopg2 import pool
from dotenv import load_dotenv


load_dotenv()

db_settings = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}


max_connections = os.getenv('DB_MAX_CONNECTIONS')
connection_pool = pool.SimpleConnectionPool(
    1, max_connections,
    **db_settings
)

