import os
import json
import psycopg2
from sqlalchemy.engine.url import make_url

# Define DATABASE_URL
DATABASE_URL = "postgresql://admin:admin@localhost:5432/datamart"

def get_database_schema() -> str:
    """
    Fetch the PostgreSQL database schema and return it as a formatted string.
    Uses DATABASE_URL for connection.
    """
    schema_info = []

    try:
        # Parse DATABASE_URL to extract credentials
        db_url = make_url(DATABASE_URL)
        conn = psycopg2.connect(
            dbname=db_url.database,
            user=db_url.username,
            password=db_url.password,
            host=db_url.host,
            port=db_url.port
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{table_name}';
            """)
            columns = cursor.fetchall()

            table_schema = {
                "table_name": table_name,
                "columns": [{"name": col[0], "type": col[1]} for col in columns],
            }
            schema_info.append(table_schema)

        cursor.close()
        conn.close()

    except Exception as e:
        return f"Error retrieving database schema: {str(e)}"

    return json.dumps(schema_info, indent=2)
