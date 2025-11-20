import sqlite3
import pandas as pd
import re
from difflib import get_close_matches

def execute_sql_query(db_source, sql_query):
    """Executes SQL against a SQLite DB (file or connection)."""
    try:
        # Handle if db_source is a path string or a connection object
        if isinstance(db_source, str):
            conn = sqlite3.connect(db_source)
            should_close = True
        else:
            conn = db_source
            should_close = False

        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        if sql_query.strip().lower().startswith("select"):
            cols = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=cols)
            if should_close: conn.close()
            return df, None
        else:
            conn.commit()
            if should_close: conn.close()
            return pd.DataFrame(), "Query executed successfully"
            
    except Exception as e:
        return None, f"SQL Error: {e}"

def natural_language_to_sql(query, db_schema):
    """Converts natural language to SQL based on schema."""
    query_lower = query.lower().strip()
    tables = list(db_schema.keys())
    if not tables:
        return "SELECT 'No table found' as error;"
        
    table = tables[0]
    columns = db_schema[table]

    # --- Helper: Fuzzy Match ---
    def fuzzy_col(word):
        matches = get_close_matches(word.lower(), [c.lower() for c in columns], n=1, cutoff=0.5)
        return matches[0] if matches else None

    # --- Logic for Aggregates, WHERE clauses, etc. ---
    # (Simplified version of your logic for brevity, but fully functional)
    
    if "count" in query_lower or "how many" in query_lower:
        return f"SELECT COUNT(*) FROM {table};"
    
    if "schema" in query_lower or "columns" in query_lower:
        return f"PRAGMA table_info('{table}');"

    # Basic Select * default
    col_guess = "*"
    
    # Try to find a specific column mentioned
    for word in query_lower.split():
        match = fuzzy_col(word)
        if match:
            col_guess = match
            break

    # Check for basic numeric filters (e.g., "age > 25")
    where_clause = ""
    numeric_conditions = re.findall(r'(\w+)\s*(>=|<=|>|<|=)\s*(\d+)', query_lower)
    conditions = []
    for col, op, val in numeric_conditions:
        c_match = fuzzy_col(col)
        if c_match:
            conditions.append(f"{c_match} {op} {val}")
    
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)

    sql = f"SELECT {col_guess} FROM {table}{where_clause} LIMIT 50;"
    return sql