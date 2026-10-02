import os
import psycopg2


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST", "postgres"),
        port=os.getenv("DATABASE_PORT", "5432"),
        database=os.getenv("DATABASE_NAME", "cloudnotes"),
        user=os.getenv("DATABASE_USER", "postgres"),
        password=os.getenv("DATABASE_PASSWORD", "postgres"),
    )
