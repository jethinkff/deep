import logging
from db_train import get_database_schema
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
import requests
import json
import pandas as pd
import re

# Configure Logging
logging.basicConfig(
    filename="query_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize FastAPI
app = FastAPI()

# PostgreSQL Database Connection
DATABASE_URL = "postgresql://admin:admin@localhost:5432/datamart"
engine = create_engine(DATABASE_URL)

# Ollama API Config
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "deepseek-r1"

def get_sql_from_natural_query(user_query: str) -> str:
    """
    Calls AI API (DeepSeek R1 via Ollama) to generate SQL from a natural language query.
    Now includes the database schema for more accurate query generation.
    """
    logging.info(f"Received query: {user_query}")

    # Fetch the latest database schema
    db_schema = get_database_schema()

    headers = {"Content-Type": "application/json"}
    data = {
        "model": "deepseek-r1",
        "prompt": f"""
        You are a PostgreSQL SQL generator. Below is the database schema:

        ```
        {db_schema}
        ```

        Based on this schema, generate a **valid** SQL query for the following question:

        "{user_query}"

        **RULES:**
        - Return ONLY the SQL query** inside triple backticks (` ```sql ... ``` `)
        - make sure there is no space between key words
        - **No explanations, no reasoning.**
        - **Ensure the query matches the provided schema.**
        - ensure the table names are correctly used from the db_schema provided
        - save the sql query to a local log file and show the direcotry of the log file.

        Now, generate the SQL query.
        """.strip()

    }
    logging.info(f"db_schema: {db_schema}")

    try:
        response = requests.post("http://127.0.0.1:11434/api/generate", headers=headers, json=data, stream=True)

        sql_query = ""
        response_text = ""
 


        for line in response.iter_lines():
            if line:
                parsed = json.loads(line.decode("utf-8"))
                response_text += parsed.get("response", "").strip() + " "
                logging.info(f"response:{parsed.get("response", "").strip() + " "}")
        logging.info(f"response_text:{response_text}")


        # Updated regex pattern with flexible spacing
        match = re.search(r"`` *sql\s*(.*?)\s*`` *", response_text, re.DOTALL)
        

        if match:
            sql_query = match.group(1).strip()

        # Log extracted SQL
        logging.info(f"Extracted SQL: {sql_query}\n")
        sql_query = fix_sql_query(sql_query)
        logging.info(f"Fixed SQL: {sql_query}\n")

        # Handle empty or invalid SQL
        if not sql_query:
            raise ValueError("AI returned an empty SQL query")

        return sql_query

    except Exception as e:
        logging.error(f"Error in get_sql_from_natural_query: {str(e)}")
        raise ValueError("SQL query generation failed")



# Query Execution Function
def execute_sql_query(sql_query: str):
    """
    Runs the generated SQL query against PostgreSQL and returns results.
    Logs execution and any errors.
    """
    try:
        logging.info(f"Executing SQL: {sql_query}")
        df = pd.read_sql(sql_query, engine)
        result = df.to_dict(orient="records")
        logging.info(f"Query Result: {result}")
        return result

    except Exception as e:
        logging.error(f"Database Error: {str(e)}")
        return {"error": str(e)}

# API Route for Querying Data Mart
@app.get("/query")
async def query_data(natural_query: str):
    """
    API endpoint to process a natural language query.
    Logs user query, AI response, generated SQL, and execution result.
    """
    try:
        sql_query = get_sql_from_natural_query(natural_query)
        if not sql_query:
            raise ValueError("SQL query generation failed")

        results = execute_sql_query(sql_query)
        return {"query": sql_query, "results": results}

    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run server with: uvicorn query_api:app --reload

def fix_sql_query(query: str) -> str:
    """
    Cleans up SQL queries by:
    - Fixing column & table names with incorrect spacing (e.g., "user _id" → "user_id").
    - Ensuring correct spacing around SQL operators (`>=`, `<=`, `!=`, `=`).
    - Formatting `INTERVAL '30 days'` correctly.
    - Keeping proper SQL readability.
    """

    # Step 1: Fix incorrect spacing in column and table names
    query = re.sub(r'(\w+)\s+_\s*(\w+)', r'\1_\2', query)
    query = re.sub(r'(\w+)\s+_(\w+)', r'\1_\2', query)  # Run twice to handle multiple spaces


    # Step 2: Ensure proper spacing around comparison operators
    query = re.sub(r'\s*(>=|<=|!=|=)\s*', r' \1 ', query)

    # Step 3: Correct INTERVAL format (fixing '3 0 days' → '30 days')
    query = re.sub(r'\b(\d)\s+(\d+)\s+days\b', r"INTERVAL '\1\2 days'", query, flags=re.IGNORECASE)
    query = re.sub(r'\b(\d)\s+(\d+)\s+days\b', r'\1\2 days', query, flags=re.IGNORECASE)


    # Step 4: Remove excessive spaces while keeping readability
    query = re.sub(r'\s+', ' ', query).strip()

    return query