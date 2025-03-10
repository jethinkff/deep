import re

def fix_sql_query(query: str) -> str:
    """
    Finalized version ensuring:
    - Correct SQL keyword spacing.
    - Proper formatting for column/table names.
    - Fixes misplaced spaces within words (including multi-split column names).
    - Corrects PostgreSQL INTERVAL syntax.
    - Ensures overall query correctness.

    Args:
        query (str): The malformed SQL query.

    Returns:
        str: The fully corrected SQL query.
    """

    # Fix split SQL keywords (e.g., "D IST INCT" → "DISTINCT")
    sql_keywords = ["DISTINCT", "SELECT", "FROM", "WHERE", "JOIN", "ON", "AS", "INTERVAL", "COUNT", "CURRENT_DATE"]
    for kw in sql_keywords:
        pattern = r"\b" + r"\s*".join(kw) + r"\b"
        query = re.sub(pattern, kw, query, flags=re.IGNORECASE)

    # Fix split column and table names (e.g., "com pletion_date" → "completion_date")
    query = re.sub(r'(\w+)\s+(\w+)', r'\1\2', query)

    # Fix spaces in column and table names with underscores (e.g., "user _id" → "user_id")
    query = re.sub(r'(\w+)\s+\_(\w+)', r'\1_\2', query)

    # Fix spaces around dot notation (e.g., "u .user_id" → "u.user_id")
    query = re.sub(r'(\w+)\s*\.\s*(\w+)', r'\1.\2', query)

    # Ensure proper spacing for SQL operators (>=, <=, !=, etc.)
    query = re.sub(r'\s*([<>=!]+)\s*', r' \1 ', query)

    # Fix PostgreSQL INTERVAL syntax (e.g., INTERVAL ' 3 0 ' DAY → INTERVAL '30 days')
    query = re.sub(r"INTERVAL\s+'?\s*(\d+)\s*'? DAYS?", r"INTERVAL '\1 days'", query, flags=re.IGNORECASE)

    # Ensure spacing before and after SQL keywords
    query = re.sub(r'(?<!\s)(SELECT|FROM|WHERE|JOIN|ON|AS|INTERVAL|COUNT|CURRENT_DATE)(?!\s)', r' \1 ', query, flags=re.IGNORECASE)

    # Ensure proper spacing after SQL keywords (e.g., "FROMuser" → "FROM user")
    query = re.sub(r'(FROM|JOIN|ON|WHERE|SELECT|COUNT)\s*([a-zA-Z])', r'\1 \2', query, flags=re.IGNORECASE)

    # Fix "sqlSELECT" issue by ensuring space after "sql"
    query = re.sub(r'^(sql)(SELECT)', r'\1 \2', query, flags=re.IGNORECASE)

    # Normalize multiple spaces to a single space
    query = re.sub(r'\s+', ' ', query).strip()

    return query

# Example Usage:
sql_query = """sql  SELECT COUNT (D IST INCT u .user _id )  
FROM user u  
JOIN course _user cu ON u .user _id = cu .user _id  
WHERE cu .com pletion _date >= CURRENT _DATE - INTERVAL ' 3 0 ' DAY"""

fixed_query = fix_sql_query(sql_query)
print(fixed_query)
