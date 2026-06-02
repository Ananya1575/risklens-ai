import sqlite3
import pandas as pd
import os
from src.utils.config import SQL_DB_PATH
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_database():
    """
    Load the cleaned CSV data and store it in a SQLite database.
    SQLite is a lightweight database that runs entirely as a file —
    no server needed. Perfect for this project.
    """
    from src.data.loader import load_and_join_all
    from src.data.preprocessor import (
        drop_useless_columns, drop_high_missing_columns,
        fill_missing_values, add_feature_engineering
    )

    logger.info("Building SQLite database for Talk-to-Data...")

    df = load_and_join_all()
    df = drop_useless_columns(df)
    df = drop_high_missing_columns(df)
    df = fill_missing_values(df)
    df = add_feature_engineering(df)

    # Keep only the readable columns for querying
    # We do NOT encode categoricals here — we want readable text values
    columns_to_keep = [
        "SK_ID_CURR", "TARGET", "NAME_CONTRACT_TYPE", "CODE_GENDER",
        "AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "AMT_GOODS_PRICE",
        "NAME_EDUCATION_TYPE", "NAME_FAMILY_STATUS", "OCCUPATION_TYPE",
        "AGE_YEARS", "YEARS_EMPLOYED", "CREDIT_INCOME_RATIO",
        "ANNUITY_INCOME_RATIO", "EXT_SOURCE_2", "EXT_SOURCE_3",
        "bureau_loan_count", "bureau_active_loans",
        "prev_app_count", "prev_approved_count", "prev_refused_count"
    ]

    # Only keep columns that exist in the dataframe
    columns_to_keep = [c for c in columns_to_keep if c in df.columns]
    df = df[columns_to_keep]

    # Save to SQLite
    os.makedirs(os.path.dirname(SQL_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(SQL_DB_PATH)
    df.to_sql("applicants", conn, if_exists="replace", index=False)
    conn.close()

    logger.info(f"Database built at {SQL_DB_PATH}")
    logger.info(f"Table 'applicants' has {len(df)} rows and {len(df.columns)} columns")
    return True


def run_sql_query(sql: str) -> pd.DataFrame:
    """
    Execute a SQL query on the SQLite database and return results as a dataframe.
    """
    if not os.path.exists(SQL_DB_PATH):
        logger.warning("Database not found — building it now...")
        build_database()

    try:
        conn = sqlite3.connect(SQL_DB_PATH)
        df_result = pd.read_sql_query(sql, conn)
        conn.close()
        logger.info(f"Query returned {len(df_result)} rows")
        return df_result

    except Exception as e:
        logger.error(f"SQL error: {e}")
        return pd.DataFrame({"error": [str(e)]})


def ask_question(question: str) -> dict:
    """
    Full pipeline — takes a plain English question,
    converts to SQL, runs it, returns readable answer.
    """
    from src.talk_to_data.nl_to_sql import question_to_sql, results_to_answer

    # Step 1 — Convert question to SQL
    sql = question_to_sql(question)

    # Step 2 — Run SQL
    df_result = run_sql_query(sql)

    # Step 3 — Format results as string for the LLM
    if df_result.empty:
        results_str = "No results found"
    else:
        results_str = df_result.head(20).to_string(index=False)

    # Step 4 — Generate human readable answer
    answer = results_to_answer(question, sql, results_str)

    return {
        "question": question,
        "sql": sql,
        "results": df_result,
        "answer": answer
    }