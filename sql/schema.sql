-- ============================================================
-- RiskLens AI — Credit Risk Intelligence Platform
-- SQLite Database Schema
-- ============================================================
-- This file documents the structure of the `applicants` table
-- used by the Talk-to-Data NL→SQL chatbot module.
-- The table is created programmatically by query_runner.py
-- from the cleaned Home Credit dataset.
-- ============================================================

CREATE TABLE IF NOT EXISTS applicants (

    -- ── Identifiers ──────────────────────────────────────────
    SK_ID_CURR              INTEGER,        -- Unique applicant ID

    -- ── Target Variable ──────────────────────────────────────
    TARGET                  INTEGER,        -- 1 = defaulted, 0 = did not default

    -- ── Loan Information ─────────────────────────────────────
    NAME_CONTRACT_TYPE      TEXT,           -- 'Cash loans' or 'Revolving loans'
    AMT_CREDIT              REAL,           -- Total loan credit amount
    AMT_ANNUITY             REAL,           -- Monthly loan annuity/repayment amount
    AMT_GOODS_PRICE         REAL,           -- Price of goods the loan is for
    AMT_INCOME_TOTAL        REAL,           -- Applicant annual income

    -- ── Demographics ─────────────────────────────────────────
    CODE_GENDER             TEXT,           -- 'M', 'F', or 'XNA'
    NAME_EDUCATION_TYPE     TEXT,           -- Highest education level
    NAME_FAMILY_STATUS      TEXT,           -- Marital status
    OCCUPATION_TYPE         TEXT,           -- Type of occupation/job
    AGE_YEARS               REAL,           -- Age in years (derived from DAYS_BIRTH)
    YEARS_EMPLOYED          REAL,           -- Years employed (derived from DAYS_EMPLOYED)

    -- ── Engineered Features ──────────────────────────────────
    CREDIT_INCOME_RATIO     REAL,           -- AMT_CREDIT / AMT_INCOME_TOTAL
    ANNUITY_INCOME_RATIO    REAL,           -- AMT_ANNUITY / AMT_INCOME_TOTAL

    -- ── External Credit Scores ───────────────────────────────
    EXT_SOURCE_2            REAL,           -- Normalised score from bureau 2 (0 to 1)
    EXT_SOURCE_3            REAL,           -- Normalised score from bureau 3 (0 to 1)

    -- ── Bureau Data (aggregated from bureau.csv) ─────────────
    bureau_loan_count       INTEGER,        -- Total loans at other institutions
    bureau_active_loans     INTEGER,        -- Currently active loans elsewhere
    bureau_avg_days_credit  REAL,           -- Average days since credit was granted

    -- ── Previous Applications (from previous_application.csv) 
    prev_app_count          INTEGER,        -- Total previous applications at Home Credit
    prev_approved_count     INTEGER,        -- Number of previously approved applications
    prev_refused_count      INTEGER         -- Number of previously refused applications

);

-- ============================================================
-- Notes:
-- • Table is populated by src/talk_to_data/query_runner.py
-- • Categorical columns retain original text values (not encoded)
--   so the LLM can generate readable WHERE clauses
-- • Numeric columns use cleaned/imputed values from preprocessor
-- • AGE_YEARS and YEARS_EMPLOYED are positive values derived
--   from DAYS_BIRTH and DAYS_EMPLOYED (originally negative)
-- ============================================================